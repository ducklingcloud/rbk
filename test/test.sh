#!/bin/bash

function case1()
{
    rm -fr testdata; tar xf testdata.tar.xz
    rm -fr bak1; mkdir bak1;
    cd bak1
    python3 ../../rbk1_plan.py ../testdata rbk_test 5
    cd ..

    if [[ -e bak1/rbk_list_0004.job ]]; then
        return 0
    fi

    echo "===> The case1 failed!"
    return 1
}

function case2()
{
    mv testdata/show_in_deleted.txt testdata/show_in_incremental.txt
    echo "test update" >> testdata/updated.txt
    
    rm -fr bak2; mkdir bak2;
    cd bak2
    python3 ../../rbk1_plan.py ../testdata rbk_test_incremental 5 ../bak1/rbk_all.dat
    cd ..

    if [[ -e bak2/rbk_list_0001.job && \
              ! -e bak2/rbk_list_0002.job ]]; then
        if grep -q show_in_deleted bak2/rbk_deleted.dat ; then
            return 0
        fi
    fi

    echo "===> The case2 failed!"
    return 1          
}

case1 && case2 && echo "All tests passed."
