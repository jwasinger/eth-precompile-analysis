from db import DB

from eth_jsonrpc_ws import EthRPCClient
import sqlite3
import asyncio

connection = sqlite3.connect('precompile_calls.db')
WS_RPC_URL='ws://localhost:8546'

cursor = connection.cursor()
# query to see if table exists:
# SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';

async def run_collection():
    rpc = EthRPCClient(WS_RPC_URL)
    async with rpc:
        db = DB.create_or_new()

        while True:
            remote_head = rpc.GetHeadBlockNumber()
            local_head = db.HeadBlockNumber()
            if remote_head > local_head:
                print("local head block nr {} greater than remote block nr {}. nothing to collect")
                return

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
