import os
import shutil
import glob
import sys
import boto3

"""
Handy deployment script to deploy lambdas from command line
"""
lambda_client = boto3.client('lambda')

def main():

    # mkdir tmp
    target_dir = './tmp_lambda_deployment_pkg'
    try:
        shutil.rmtree(target_dir)
    except OSError:
        pass
    os.mkdir(target_dir)

    # install deps
    cmd = 'pip install matplotlib --target=%s' % target_dir
    os.system(cmd)

    # add lambda script
    os.chdir(target_dir)

    for i, lamf in enumerate(['CoffeeCalc.py', 'CoffeeTracker.py']):
        print('#########################################################')
        # remove the previous fn main script if deploying multiple
        if glob.glob('./*.py'):
            os.remove(glob.glob('./*.py')[0])

        # add main script to top level dir
        shutil.copy2('../' + lamf, './')

        # zip zip
        zipf = './lambda_pkg'
        shutil.make_archive(zipf, 'zip', root_dir='.', base_dir='.')

        # deploy
        function_name = lamf.rsplit('.', 1)[0].rsplit('/', 1)[1]
        response = _lam.update_function_code(function_name, zipf+'.zip')

    os.chdir('..')
    cmd = 'rm -r %s' % target_dir
    os.system(cmd)
    return


def update_function_code(fn, zip_bytes, publish=False):
    """
    This API code updates the $LATEST (Unassigned) lambda function version
    If publish = True, a new numbered version is also published.
    """

    with open(zip_bytes, 'rb') as content_file:
        content = content_file.read()

    response = lambda_client.update_function_code(
            FunctionName=fn,
            ZipFile=content,
            Publish=publish
    )
    return response


if __name__ == '__main__':
    sys.exit(main())
