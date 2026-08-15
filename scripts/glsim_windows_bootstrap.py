"""Start GLSim after applying the project-local Windows fd cleanup fix."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from support.windows_gltest_compat import install


install()

from glsim.__main__ import main


if __name__ == "__main__":
    main()
