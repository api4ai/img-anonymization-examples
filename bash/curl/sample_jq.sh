#!/bin/bash

######################################################
# NOTE:                                              #
#   This script requires "jq" and "tr" command line  #
#   tools!     										 #
#   See:											 #
#		https://stedolan.github.io/jq/				 #
#       https://www.gnu.org/software/coreutils/		 #
######################################################


IMAGE=${1}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run base sample script to get raw output.
raw_response=$(bash ${DIR}/sample.sh "${IMAGE}")

# Parse response in three steps.

# 1. Print hidden objects.
echo "💬 Hidden objects:"
jq ".results[0].entities[1].objects" <<< ${raw_response}

# 2. Get response image's format.
OUTPUT_IMAGE_FORMAT=$(jq -r ".results[0].entities[0].format" <<< ${raw_response})
OUTPUT_IMAGE="result.${OUTPUT_IMAGE_FORMAT}"

# 3.  Save image to the file.
jq -r ".results[0].entities[0].image" <<< ${raw_response} | base64 -d > "${OUTPUT_IMAGE}"
echo "💬 The ${OUTPUT_IMAGE} image is saved to the current directory."
