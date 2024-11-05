import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.append(src_dir)

import crepo.crepo as crepo

if __name__ == "__main__":
    crepo.main()
