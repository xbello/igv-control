"""Provide access through command line to IGV controlling."""
import helpers


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
        pass


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

    import readchar

    print("Press <- or ->, q to quit")

    while True:
        c = readchar.readkey()
        LEFT = readchar.key.LEFT
        RIGHT = readchar.key.RIGHT

        if c in ("q", "Q",
                 readchar.key.CTRL_C,
                 readchar.key.CTRL_D,
                 readchar.key.CTRL_Z):
            break
        if c in (LEFT, RIGHT):
            print("Seems OK")
