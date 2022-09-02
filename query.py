from eth_jsonrpc_ws import EthRPCClient
import sqlite3
import asyncio
import json

from db import DB
from common import PrecompileCall

import sys
sys.setrecursionlimit(4000)

import time

WS_RPC_URL='ws://localhost:8546'

PRECOMPILED_ADDRS = {
    '0x0000000000000000000000000000000000000001', # ecrecover
    '0x0000000000000000000000000000000000000002', # sha256
    '0x0000000000000000000000000000000000000003', # ripemd
    '0x0000000000000000000000000000000000000004', # data copy (identity)
    '0x0000000000000000000000000000000000000005', # modexp
    '0x0000000000000000000000000000000000000006', # bn256 add
    '0x0000000000000000000000000000000000000007', # bn256 scalar mul
    '0x0000000000000000000000000000000000000008', # bn256 pairing
    '0x0000000000000000000000000000000000000009', # blake2f
}

async def has_txs(rpc, block_num):
    block = await rpc.eth_getBlockByNumber(block_num)
    return len(block['transactions']) > 0

async def find_precompile_calls(rpc, block_num):
    calls = []
    block = await rpc.eth_getBlockByNumber(block_num)
    for tx_hash in block['transactions']:
        result = await rpc.debug_traceTransaction(tx_hash)
        if result == 'bad':
            import pdb; pdb.set_trace()
            result2 = await rpc.debug_traceTransaction(tx_hash)

        if len(result) > 0:
            print("precompiles!")
        else:
            continue

        for idx, call in enumerate(result):
            assert 'to' in call and call['to'] in PRECOMPILED_ADDRS

            call_input = ''
            call_output = ''

            # only record input/output for modexp
            if call['to'] == '0x0000000000000000000000000000000000000005':
                call_input = call['input']
                call_output = call['output']

            precompile_call = PrecompileCall(
                call['to'],
                call['from'],
                call_input,
                call_output,
                call['gasUsed'],
                tx_hash,
                idx,
                call['type'])
            calls.append(precompile_call)

    return calls

async def run_collection():
    rpc = EthRPCClient(WS_RPC_URL)
    async with rpc:
        db = DB.create_or_new()
        local_head = db.HeadBlockNumber()
        if local_head == 0:
            remote_head = int(await rpc.eth_blockNumber(), 16)
            local_head = remote_head - 5
            db.SetHeadBlockNumber(local_head)

        while True:
            remote_head = int(await rpc.eth_blockNumber(), 16) - 5
            local_head = db.HeadBlockNumber()
            if remote_head < local_head:
                print("local head block number {} greater than remote block number {}. nothing to collect")
                return
            elif remote_head == local_head:
                print("up to date with node. sleeping 10s...")
                time.sleep(10)
                continue

            print("doing collection")

            for block_num in range(local_head + 1, remote_head + 1):
                print(block_num)
                should_examine = await has_txs(rpc, block_num)
                if should_examine:
                    precompile_calls = await find_precompile_calls(rpc, block_num)
                    if len(precompile_calls) > 0:
                        db.AddPrecompileCalls(block_num, precompile_calls)

                db.SetHeadBlockNumber(block_num)
            # for each block number in range(local_head + 1, remote_head + 1):
                # for each tx in block:
                    # trace = ....
                    # calls = extract_precompile_calls(trace)
                    # for call in calls:
                    #   db.SetPrecompileCall(...)
                # db.SetHeadBlock(block number)

            #for block in range(local_head + 1, remote_head + 1):
            #    pass

def main():
    asyncio.get_event_loop().run_until_complete(run_collection())

if __name__ == "__main__":
    main()
