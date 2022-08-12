from eth_jsonrpc_ws import ETHRPCClient
import sqlite3

connection = sqlite3.connect('precompile_calls.db')

cursor = connection.cursor()
# query to see if table exists:
# SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';

def db_exists():
    pass

def run_collection(db):
    head = rpc.GetHeadBlockNumber()
    local_head = db.HeadBlock().Number
    if head > local_head:
        print("local head block nr {} greater than remote block nr {}. nothing to collect")
        return

    # for each block number in range(local_head + 1, remote_head + 1):
        # for each tx in block:
            # trace = ....
            # calls = extract_precompile_calls(trace)
            # for call in calls:
            #   db.SetPrecompileCall(...)
        # db.SetHeadBlock(block number)

def main():
    async with ETHRPCClient as rpc:
        db = DB.create_or_new()

        while True:
            run_collection(db)

if __name__ == "__main__":
    main()
