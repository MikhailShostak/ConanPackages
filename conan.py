import os
import subprocess
import sys
import json

ARTIFACTORY_URL = os.environ.get('ARTIFACTORY_URL', None)
ARTIFACTORY_USER = os.environ.get('ARTIFACTORY_USER', None)
ARTIFACTORY_KEY = os.environ.get('ARTIFACTORY_KEY', None)
ARTIFACTORY_NAME = 'artifactory' if ARTIFACTORY_URL else None

ADDITIONAL_CONAN_COMMANDS = [arg for arg in ['--keep-source', '--keep-build'] if arg in sys.argv]

BUILD_DIR = os.environ.get('BUILD_DIR', '.build')
ARCHITECTURES = [os.environ['BUILD_ARCHITECTURE']] if 'BUILD_ARCHITECTURE' in os.environ else ['x86_64']
CONFIGURATIONS = [os.environ['BUILD_CONFIGURATION']] if 'BUILD_CONFIGURATION' in os.environ else ['Release', 'Debug']

UNSECURE_DRY_RUN = '--unsecure-dry-run' in sys.argv
DRY_RUN = UNSECURE_DRY_RUN or '--dry-run' in sys.argv

CI_STEPS = '--ci-steps' in sys.argv


def run(command, *args, force=False, secure=False, **kwargs):
    if not secure or UNSECURE_DRY_RUN:
        print(*command, *args, **kwargs)
    if force or not DRY_RUN:
        subprocess.check_call(command, *args, **kwargs)


def create_package(package, profile):
    conan_command = ['conan', 'create', package, '--profile', profile] + ADDITIONAL_CONAN_COMMANDS
    run(conan_command)


if '--info' in sys.argv:
    run(['conan', 'search'], force=True)
    run(['conan', 'profile', 'list'], force=True)
    run(['conan', 'remote', 'list'], force=True)

if CI_STEPS or '--install-conan' in sys.argv:
    run([sys.executable, '-m', 'pip', 'install', 'conan'])

if ARTIFACTORY_URL and (CI_STEPS or '--add-artifactory' in sys.argv):
    run(['conan', 'remote', 'add', ARTIFACTORY_NAME, ARTIFACTORY_URL])

if '--logout' in sys.argv:
    run(['conan', 'user', '-c'])

if ARTIFACTORY_KEY and (CI_STEPS or '--login' in sys.argv):
    run(['conan', 'user', '-p', ARTIFACTORY_KEY, '-r', ARTIFACTORY_NAME, ARTIFACTORY_USER], secure=True)

packages = []
receipts = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f == 'conanfile.py':
            packages.append(root)
            package_info = json.loads(subprocess.check_output(['conan', 'inspect', root, '--format=json'], encoding='utf-8'))
            receipts.append(package_info['name'] + '/' + package_info['version'])


for arch in ARCHITECTURES:
    for config in CONFIGURATIONS:
        profile = config + '-' + arch
        if CI_STEPS or '--create-profiles' in sys.argv:
            run(['conan', 'profile', 'detect', '--force', '--name', profile])
            run(['conan', 'profile', 'update', 'settings.build_type=' + config, profile])
            run(['conan', 'profile', 'update', 'settings.arch=' + arch, profile])
            run(['conan', 'profile', 'update', 'settings.arch_build=' + arch, profile])
            if 'BUILD_COMPILER' in os.environ and 'BUILD_COMPILER_VERSION' in os.environ:
                run(['conan', 'profile', 'update', 'settings.compiler=' + os.environ['BUILD_COMPILER'], profile])
                run(['conan', 'profile', 'update', 'settings.compiler.version=' + os.environ['BUILD_COMPILER_VERSION'], profile])
            if 'BUILD_STDLIB' in os.environ:
                run(['conan', 'profile', 'update', 'settings.compiler.libcxx=' + os.environ.get('BUILD_STDLIB'), profile])

        if CI_STEPS or '--install-packages' in sys.argv:
            run(['conan', 'install', '.', '-if', os.path.join(BUILD_DIR, profile)] + ['--profile', profile, '--update', '--build=missing'])

        if CI_STEPS or '--create-packages' in sys.argv:
            for package in packages:
                create_package(package, profile)

if ARTIFACTORY_NAME and (CI_STEPS or '--deploy' in sys.argv):
    for r in receipts:
        run(['conan', 'upload', r, '--all', '-r', ARTIFACTORY_NAME] + ['-c'] if CI_STEPS else [])
