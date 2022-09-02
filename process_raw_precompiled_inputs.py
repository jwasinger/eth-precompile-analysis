def main():
    for (sender, input_data, gas_used) in modexp_calls:
        base_size, exponent_size, modulus_size, base, exponent, modulus = proc_input_data(input_data)

        if base_size > modulus_size:
            pass # bad, won't work with evmmax
        if base > modulus:
            pass # bad, won't work with evmmax
        if modulus % 2 == 0:
            pass # bad, won't work with evmmax
        if exponent_size >= 32:
            pass # note down

        # note down this with the contract:
        # insert into modexp_calls (base_size, modulus_size, exponent_size, base, modulus, exponent)
    pass

if __name__ == "__main__":
    main()
