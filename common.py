class PrecompileCall():
    def __self__(recipient: str, sender: str, input_data: str, output_data: str, gas_used: int, tx_hash: str, idx: int):
        self.recipient = recipient
        self.sender = sender
        self.input_data = input_data
        self.output_data = output_data
        self.gas_used = gas_used
        self.tx_hash = tx_hash
        self.idx = idx
