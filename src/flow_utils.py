import functools


# Add decorator for installation from pip rather than conda
# see https://github.com/Netflix/metaflow/issues/24
def pip(libraries):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            import subprocess
            import sys

            for library, version in libraries.items():
                print("Pip Install:", library, version)
                subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", library + "==" + version])
            return function(*args, **kwargs)

        return wrapper

    return decorator
