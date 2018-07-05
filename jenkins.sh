# Check pycodestyle based on hpcnt-ml/.flake8
function run_flake8() {
    flake8
    is_flake8_pass=$?
    if [ ${is_flake8_pass} -ne 0 ]; then
        echo "Test Fail! | check flake8"
        exit 1
    fi
}

function run_pytest() {
    pytest
    is_pytest_pass=$?
    if [ ${is_pytest_pass} -ne 0 ]; then
        echo "Test Fail! | check pytest"
        exit 1
    fi
}


run_flake8
run_pytest
