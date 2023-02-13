from portfolio_allocation.non_blend_fund_asset_allocation import (
    generate_combined_non_blend_fund_asset_allocation,
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
