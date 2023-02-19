# pylint: disable=pointless-string-statement
"""This is the entry point to the python program."""
from portfolio_allocation.non_blend_fund_asset_allocation import (
    generate_combined_non_blend_fund_asset_allocation,
)
from portfolio_allocation.blend_fund_asset_allocation import (
    generate_combined_blend_fund_asset_allocation,
)

from portfolio_allocation.combined_asset_allocation import (
    combine_all_asset_allocation,
    generate_asset_allocation_by_asset_class_table,
    generate_asset_allocation_by_region_and_asset_class_table,
)
from portfolio_allocation.generate_html_outputs import (
    update_asset_allocation_html,
    open_local_html,
)

if __name__ == "__main__":
    """
    step1: retrieve non blend fund
    step2: retrieve blend fund:
        for a given asset account name:
        1. retrieve asset allocation mappings from crawler.
        2. retrieve a set of attributes for the account.
        3. Use the properly mapped callable to get the asset information
        for the specific account.
    step3: combine blend funds and create html table.
    step4: open html table.
    """
    non_blend_fund_asset_allocation = (
        generate_combined_non_blend_fund_asset_allocation()
    )
    blend_fund_asset_allocation = generate_combined_blend_fund_asset_allocation()
    all_asset_allocation = combine_all_asset_allocation(
        blend_fund_asset_allocation=blend_fund_asset_allocation,
        non_blend_fund_asset_allocation=non_blend_fund_asset_allocation,
    )
    asset_allocation_by_asset_class_table = (
        generate_asset_allocation_by_asset_class_table(
            all_asset_allocation=all_asset_allocation,
        )
    )
    asset_allocation_by_region_and_asset_class_table = (
        generate_asset_allocation_by_region_and_asset_class_table(
            asset_allocation_by_asset_class_table=asset_allocation_by_asset_class_table,
        )
    )
    update_asset_allocation_html(
        asset_table_without_region=asset_allocation_by_asset_class_table,
        asset_table_with_region=asset_allocation_by_region_and_asset_class_table,
    )
    open_local_html()
