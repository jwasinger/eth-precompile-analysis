from db import DB

from eth_jsonrpc_ws import EthRPCClient
import sqlite3
import asyncio

WS_RPC_URL='ws://localhost:8546'

async def has_txs(rpc, block_num):
    block = await rpc.eth_getBlockByNumber(block_num)
    return len(block['transactions']) > 0

def parse_trace(trace_files: [str]):
    for trace_file in trace_files:
        with open(trace_file) as f:
            for line in f:
                # if it is a 'result' line, it is the end of a transaction
                # flush the current-tx results

                # else it's a trace step for a transaction
    pass

async def find_precompile_calls(rpc, block_num):
    block = await rpc.eth_getBlockByNumber(block_num)
    trace_files = await rpc.debug_standardTraceBlockToFile(block['hash'])
    for file_name in trace_files:
        print(file_name)
        with open(file_name) as f:
            lines = f.readlines()
            if len(lines) > 1:
                print(lines)

async def run_collection():
    rpc = EthRPCClient(WS_RPC_URL)
    async with rpc:
        db = DB.create_or_new()

        while True:
            remote_head = int(await rpc.eth_blockNumber(), 16)
            local_head = db.HeadBlockNumber()
            if remote_head < local_head:
                print("local head block number {} greater than remote block number {}. nothing to collect")
                return

            print("doing collection")

            for block_num in range(local_head + 1, remote_head + 1):
                print(block_num)
                should_examine = await has_txs(rpc, block_num)
                if should_examine:
                    await find_precompile_calls(rpc, block_num)

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
