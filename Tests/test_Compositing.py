#region ============================ Imports =============================

import unittest
import sys
import os

# Add the project root to PYTHONPATH for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

#endregion



if __name__ == '__main__':
    unittest.main(verbosity=2)
