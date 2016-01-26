"""Provide access through command line to IGV controlling."""
import readchar

import helpers


def move_index(index, max_point):
    """Return the new index according to the key pressed."""

    c = readchar.readkey()

    if c in ("q", "Q",
             readchar.key.CTRL_C,
             readchar.key.CTRL_D,
             readchar.key.CTRL_Z):
        return "QUIT"
    elif c == (readchar.key.RIGHT):
        if index < max_point:
            index += 1
    elif c == (readchar.key.LEFT):
        if index > 0:
            index -= 1

    return index


def text_mode(variants):
    """Launch the IVG-control in text mode."""
    controller = helpers.IGV()

    # Test the IGV is running and accepting
    try:
        controller.check_igv()
    except OSError:
        # Be mild about timeouts because IGV timeouts a lot.
        print("IGV was not detected " +
              "on ip {}, port {}".format(controller.host,
                                         controller.port))

    print("Press <- or ->, [q] to quit")

    all_variants = list(variants)

    index = 0
    while True:
        index = move_index(index, len(all_variants))

        if index == "QUIT":
            break

        try:
            this_variant = all_variants[index]
            controller.goto(":".join(this_variant))
        except IndexError:
            # The list overflowed on the right.
            print("No more variants to view. Press [q] to quit")
        except OSError:
            # IGV is flawed somehow in the socket connection.
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
