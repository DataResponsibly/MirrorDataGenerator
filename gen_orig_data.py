import os, argparse
from gen_utils import readFromJson, generate_data

def run_generation(args):
    desp_data = readFromJson(args.para_file)

    for ri in range(1, args.run+1):
        generate_data(os.path.join(args.repo_dir, args.data_flag)+"/R" + str(ri) + ".csv", desp_data, src_data=args.src_data)
        if args.verbose:
            print("--- Save data in " + os.path.join(args.repo_dir, args.data_flag)+"/R" + str(ri) + ".csv" + " --- \n")

if __name__ == "__main__":
    repo_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description="Run Synthetic Data Generation")

    parser.add_argument("--data_flag", type=str)

    parser.add_argument("--para_file", type=str)

    parser.add_argument("--src_data", type=str, default=None) # for semi-real data

    parser.add_argument("--run", type=int, help="number of synthetic datasets", default=20)

    parser.add_argument('--verbose', type=bool, default=True)


    args = parser.parse_args()
    args.repo_dir = repo_dir + "/out/"

    run_generation(args)