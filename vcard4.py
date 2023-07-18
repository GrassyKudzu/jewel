def generate_vcard(name, email, phone, address):
    vcard = f"BEGIN:VCARD\nVERSION:4.0\nFN:{name}\nN:{name};;;\nEMAIL:{email}\nTEL:{phone}\nADR:{address}\nEND:VCARD"
    return vcard

def read_input_file(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def main():
    input_file = 'input.txt'
    output_file = 'output.vcf'

    try:
        name, email, phone, address = read_input_file(input_file)
        vcard_data = generate_vcard(name, email, phone, address)

        with open(output_file, 'w') as file:
            file.write(vcard_data)

        print("VCard 4.0 data has been successfully generated.")
        print(f"Output file: {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    main()
