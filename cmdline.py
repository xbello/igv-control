"""Provide access through command line to IGV controlling."""
import readchar

import helpers


def text_mode(variants):
    """Launch the IVG-control in text mode."""
    controller = helpers.IGV()

    # Test the IGV is running and accepting
    if not controller.check_igv():
        raise OSError("IGV is not running or not accepting connections\n"
                      "on ip {}, port {}".format(controller.host,
                                                 controller.port))

    print("Press <- or ->, q to quit")
    passed_variants = []

    for variant in variants:
        c = readchar.readkey()
        print(readchar.key.RIGHT)
        print(c)

        if c in ("q", "Q",
                 readchar.key.CTRL_C,
                 readchar.key.CTRL_D,
                 readchar.key.CTRL_Z):
            break
        if c == (readchar.key.RIGHT):
            # Push the variant in the old bucket
            passed_variants.append(variant)
            # TODO Send the query to the IGV
            print(variant)
        if c == (readchar.key.LEFT):
            # TODO Retrieve the last variant from the old bucket
            pass


def main(cmd_args):
    """Launch the controller either through tkinter or command line."""
    if cmd_args.gui:
        # Here we launch the GUI.
        pass
    else:
        if not cmd_args.variants:
            # No GUI and no FilePath provided.
            variants_path = input(
                "Enter the file path (or quit with [q]): ")
            if variants_path.lower() == "q":
                return False
            cmd_args.variants = variants_path

        variants = helpers.Variants(cmd_args.variants)

        # Here we launch the command line with variants.")
        text_mode(variants)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage IGV through sockets.")
    parser.add_argument("--variants",
                        help="Path to file with variants. It works with VCF " +
                        "or TAB files.")
    parser.add_argument("--gui", type=bool,
                        help="Launch a Tkinter Gui to control IGV")
    args = parser.parse_args()

    main(args)
