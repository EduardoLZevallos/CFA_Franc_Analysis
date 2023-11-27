CFA_FRANC_ZONE = [
    "Benin",  # west
    "Burkina Faso",  # west
    "Côte d'Ivoire",  # west
    "Guinea-Bissau",  # west - joins in 1997
    "Mali",  # west - joins in 1984
    "Niger",  # west
    "Senegal",  # west
    "Togo",  # west
    "Cameroon",  # middle
    "Central African Republic",  # middle
    "Chad",  # middle
    "Congo, Republic of ",  # middle
    "Equatorial Guinea",  # middle - joins in 1985
    "Gabon",  # middle
]

WEST_AFRICA = [
    "Cabo Verde",  # West
    "Gambia, The",  # West
    "Ghana",  # West
    "Guinea",  # West
    "Liberia",  # West
    "Mauritania",  # West
    "Sierra Leone",  # West
    "Nigeria",  # Western
]

MIDDLE_AFRICA = [
    "São Tomé and Príncipe",  # middle
    "Angola",  # middle
    "Congo, Dem. Rep. of the",  # middle
]

NORTH_AFRICA = [
    "Algeria",  # Northern
    "Egypt",  # Northern
    "Libya",  # Northern
    "Morocco",  # Northern
    "Sudan",  # Northern
    "Tunisia",  # Northern
]

EASTERN_AFRICA = [
    "Burundi",  # Eastern
    "Comoros",  # Eastern # In the CFA zone
    "Djibouti",  # Eastern
    "Eritrea",  # Eastern
    "Ethiopia",  # Eastern
    "Kenya",  # Eastern
    "Madagascar",  # Eastern
    "Malawi",  # Eastern
    "Mauritius",  # Eastern
    "Mozambique",  # Eastern
    "Rwanda",  # Eastern
    "Seychelles",  # Eastern
    "Somalia",  # Eastern
    "South Sudan, Republic of",  # Eastern
    "Tanzania",  # Eastern
    "Uganda",  # Eastern
    "Zambia",  # Eastern
    "Zimbabwe",  # Eastern
]

SOUTH_AFRICA = [
    "Botswana",  # South
    "Eswatini",  # South
    "Lesotho",  # South
    "Namibia",  # South
    "South Africa",  # South
]

MISSING_COUNTRIES = [
    "Canary Islands (Spain)"  # Northern
    "Ceuta (Spain)"  # Northern
    "Madeira (Portugal)"  # Northern
    "Melilla (Spain)"  # Northern
    "Western Sahara"  # Northern
    "French Southern and Antarctic Lands (France)"  # Eastern
    "Mayotte (France)"  # Eastern
    "Reunion (France)"  # Eastern
    "Somaliland (Somalia)"  # Eastern
]

"""
# SKIP_INDICATORS because missing data as of 11/12/23
- General Government Net Lending/borrowing
	cfa - 162
	west africa - 118
	middle africa - 52 
 
- General Government Gross Debt 
	cfa 223
	west africa 128
	middle africa 61
 
- Beverages, Tobacco 
	cfa 153
	west africa 134
	middle africa 49
 
- Mineral Fuels, Lubricants And Related Materials 
	cfa 183
	west africa 104
	middle africa 36

- Animal, Vegetable Oils, Fats
	cfa 168
	west africa 89
	middle africa 52

- Chemicals comparison
	cfa 94
	west africa 54
	middle africa 21

- Commodity & Transactions Not Classified Accord To Kind
	cfa 174
	west africa 122
	middle africa 59

- Gross Debt Position
	cfa 94
	west africa 48
	middle africa 31 
"""
SKIP_INDICATORS = {'GGXCNL_NGDP', 'GGXWDG_NGDP', 'SITC1_1', 'SITC1_3','SITC1_4', 'SITC1_5', 'SITC1_9', 'G_XWDG_G01_GDP_PT'}

UNIT_FORMATTING = {
    "Billions of U.S. dollars": "Billions of U.S. dollars",
    "U.S. dollars per capita": "U.S. dollars per capita",
    "Purchasing power parity; billions of international dollars": "Purchasing power parity; \n billions of international dollars",
    "Purchasing power parity; international dollars per capita": "Purchasing power parity; \n international dollars per capita",
    "Purchasing power parity; \n billions of international dollars": "Purchasing power parity; \n billions of international dollars",
    "Percent of World": "% of World",
    "National currency per international dollar": "National currency per international dollar",
    "Annual percent change": "% change",
    "Millions of people": "Millions of people",
    "Billions of U.S. dollars": "Billions of U.S. dollars",
    "Percent of GDP": "% of GDP",
    "Percent": "%",
    "% of GDP": "% of GDP",
    "Index": "Index",
    "Millions of US Dollars": "Millions of US Dollars",
    "Percent": "Percent",
    "Units": "Units",
    "Unit": "Units",
    "Index": "Index",
    "% of Potential GDP": "% of Potential GDP",
    "Months of imports of goods and services": "Months of imports of goods & services",
    "Annual Average Index, 2010 = 100": "Annual Average Index, 2010 = 100",
    "Annual average percent change": "Annual average % change",
    "Index, 2010 = 100": "Index, 2010 = 100",
}

LABEL_FORMATTING = {
    "Animal and vegetable oils and fats": "Animal, Vegetable Oils, Fats",
    "Beverages and tobacco": "Beverages, Tobacco",
    "Bond openness index (1=fully liberalized)": "Bond Openness Index (1=fully Liberalized)",
    "Broad Money (% of GDP)": "Broad Money",
    "Broad Money Growth": "Broad Money Growth",
    "Central Government Debt": "Central Government Debt",
    "Chemicals": "Chemicals",
    "Claims on Nonfinancial Private Sector (% of GDP)": "Claims On Nonfinancial Private Sector",
    "Claims on Nonfinancial Private Sector (%)": "Claims On Nonfinancial Private Sector",
    "Collective investment openness index (1=fully liberalized)": "Collective Investment Openness Index (1=fully Liberalized)",
    "Commercial credit openness index (1=fully liberalized)": "Commercial Credit Openness Index (1=fully Liberalized)",
    "Commodity & transactions not classified accord to kind": "Commodity & Transactions Not Classified Accord To Kind",
    "Consumer Prices, Average (Annual % Change)": "Consumer Prices, Average",
    "Consumer Prices, End of Period (Annual % Change)": "Consumer Prices, End Of Period",
    "Crude materials, inedible, except fuels": "Crude Materials, Inedible, Except Fuels",
    "Current account balance\nU.S. dollars": "Current Account Balance",
    "Current account balance, percent of GDP": "Current Account Balance",
    "Cyclically adjusted balance": "Cyclically Adjusted Balance",
    "Cyclically adjusted primary balance": "Cyclically Adjusted Primary Balance",
    "DEBT": "Debt",
    "Debt Forgiveness": "Debt Forgiveness",
    "Debt Securities Assets": "Debt Securities Assets",
    "Debt Securities Liabilities": "Debt Securities Liabilities",
    "Derivative investment openness index (1=fully liberalized)": "Derivative Investment Openness Index (1=fully Liberalized)",
    "Direct Investment Abroad": "Direct Investment Abroad",
    "Direct Investment In Country": "Direct Investment In Country",
    "Direct investment liquidation openness index (1=fully liberalized)": "Direct Investment Liquidation Openness Index (1=fully Liberalized)",
    "Direct investment openness index (1=fully liberalized)": "Direct Investment Openness Index (1=fully Liberalized)",
    "Equity Securities Assets": "Equity Securities Assets",
    "Equity Securities Liabilities": "Equity Securities Liabilities",
    "Equity openness index (1=fully liberalized)": "Equity Openness Index (1=fully Liberalized)",
    "Expenditure": "Expenditure",
    "Export Diversification Index": "Export Diversification Index",
    "Export Quality Index": "Export Quality Index",
    "Exports of Goods and Services (% of GDP)": "Exports Of Goods And Services",
    "Extensive Margin": "Extensive Margin",
    "External Current Account, Incl.Grants (% of GDP)": "External Current Account, Incl.grants",
    "External Debt, Official Debt, Debtor Based (% of GDP)": "External Debt, Official Debt, Debtor Based",
    "Financial Derivatives": "Financial Derivatives",
    "Financial Market Openness Index (equity, bond, money market, collective investment, derivates) 1=fully liberalized": "Financial Market Openness Index (equity, Bond, Money Market, Collective Investment, Derivates) 1=fully Liberalized",
    "Financial credit openness index (1=fully liberalized)": "Financial Credit Openness Index (1=fully Liberalized)",
    "Fiscal Council Indicator": "Fiscal Council Indicator",
    "Fiscal Rule Indicator": "Fiscal Rule Indicator",
    "Food and live animals": "Food And Live Animals",
    "GDP based on PPP, share of world": "GDP Based On PPP, Share Of World",
    "GDP per capita, current prices": "GDP Per Capita, Current Prices",
    "GDP per capita, current prices\n": "GDP Per Capita, Current Prices",
    "GDP, current prices": "GDP, Current Prices",
    "Gender Budgeting Indicator": "Gender Budgeting Indicator",
    "Gender Development Index (GDI) Time Consistent": "Gender Development Index (gdi) Time Consistent",
    "Gender Inequality Index (GII) Time Consistent": "Gender Inequality Index (gii) Time Consistent",
    "General Government Debt": "General Government Debt",
    "General government gross debt": "General Government Gross Debt",
    "General government net lending/borrowing": "General Government Net Lending/borrowing",
    "Government Debt (% of GDP)": "Government Debt",
    "Government Expenditure (% of GDP)": "Government Expenditure",
    "Government Revenue, Excluding Grants (% of GDP)": "Government Revenue, Excluding Grants",
    "Government expenditure, percent of GDP": "Government Expenditure",
    "Government primary balance, percent of GDP": "Government Primary Balance",
    "Government primary expenditure, percent of GDP": "Government Primary Expenditure",
    "Government revenue, percent of GDP": "Government Revenue",
    "Gross National Savings (% of GDP)": "Gross National Savings",
    "Gross debt position": "Gross Debt Position",
    "Gross public debt, percent of GDP": "Gross Public Debt",
    "Guarantee openness index (1=fully liberalized)": "Guarantee Openness Index (1=fully Liberalized)",
    "Household debt, all instruments": "Household Debt, All Instruments",
    "Household debt, loans and debt securities": "Household Debt, Loans And Debt Securities",
    "Implied PPP conversion rate": "Implied PPP Conversion Rate",
    "Imports of Goods and Services (% of GDP)": "Imports Of Goods And Services",
    "Inflation rate, average consumer prices": "Inflation Rate, Average Consumer Prices",
    "Inflation rate, end of period consumer prices": "Inflation Rate, End Of Period Consumer Prices",
    "Intensive Margin": "Intensive Margin",
    "Interest paid on public debt, percent of GDP": "Interest Paid On Public Debt",
    "Machinery and transport equipment": "Machinery And Transport Equipment",
    "Manufact goods classified chiefly by material": "Manufact Goods Classified Chiefly By Material",
    "Mineral fuels, lubricants and related materials": "Mineral Fuels, Lubricants And Related Materials",
    "Miscellaneous manufactured articles": "Miscellaneous Manufactured Articles",
    "Money market openness index (1=fully liberalized)": "Money Market Openness Index (1=fully Liberalized)",
    "Net Foreign Direct Investment (% of GDP)": "Net Foreign Direct Investment",
    "Net debt": "Net Debt",
    "Net lending/borrowing (also referred as overall balance)": "Net Lending/borrowing (also Referred As Overall Balance)",
    "Nominal Effective Exchange Rates (2010=100)": "Nominal Effective Exchange Rates",
    "Nominal GDP": "Nominal GDP",
    "Nonfinancial Public Sector Debt": "Nonfinancial Public Sector Debt",
    "Nonfinancial corporate debt, all instruments": "Nonfinancial Corporate Debt, All Instruments",
    "Nonfinancial corporate debt, loans and debt securities": "Nonfinancial Corporate Debt, Loans And Debt Securities",
    "Nonresident Openness Index (1=fully liberalized)": "Nonresident Openness Index (1=fully Liberalized)",
    "Openness of Capital Inflows Index  (1=fully liberalized)": "Openness Of Capital Inflows Index (1=fully Liberalized)",
    "Openness of Capital Outflows Index   (1=fully liberalized)": "Openness Of Capital Outflows Index (1=fully Liberalized)",
    "Other Investment Assets": "Other Investment Assets",
    "Other Investment Liabilities": "Other Investment Liabilities",
    "Overall Fiscal Balance, Excluding Grants (% of GDP)": "Overall Fiscal Balance, Excluding Grants",
    "Overall Fiscal Balance, Including Grants (% of GDP)": "Overall Fiscal Balance, Including Grants",
    "Overall Openness Index (all asset categories)": "Overall Openness Index (all Asset Categories)",
    "Personal capital transaction openness index (1=fully liberalized)": "Personal Capital Transaction Openness Index (1=fully Liberalized)",
    "Population": "Population",
    "Portfolio Investment Assets": "Portfolio Investment Assets",
    "Portfolio Investment Liabilities": "Portfolio Investment Liabilities",
    "Primary net lending/borrowing (also referred as primary balance)": "Primary Net Lending/Borrowing",
    "Private Inflows excluding Direct Investment": "Private Inflows Excluding Direct Investment",
    "Private Inflows excluding Direct Investment (% of GDP)": "Private Inflows Excluding Direct Investment (% Of GDP)",
    "Private Outflows excluding Direct Investment": "Private Outflows Excluding Direct Investment",
    "Private Outflows excluding Direct Investment (% of GDP)": "Private Outflows Excluding Direct Investment (% Of GDP)",
    "Private debt, all instruments": "Private Debt, All Instruments",
    "Private debt, loans and debt securities": "Private Debt, Loans And Debt Securities",
    "Proxy for Official Other Investment Liabilities": "Proxy For Official Other Investment Liabilities",
    "Public Sector Debt": "Public Sector Debt",
    "Ratio of reserve/ARA metric ": "Ratio Of Reserve/ara Metric",
    "Real Effective Exchange Rates (2010=100)": "Real Effective Exchange Rates",
    "Real GDP Growth": "Real GDP Growth Rate",
    "Real GDP growth": "Real GDP Growth Rate",
    "Real GDP growth rate, percent": "Real GDP Growth Rate",
    "Real Non-Oil GDP Growth": "Real Non-oil GDP Growth",
    "Real Per Capita GDP Growth": "Real GDP Growth Rate, per capita",
    "Real estate capital transaction openness index (1=fully liberalized)": "Real Estate Capital Transaction Openness Index (1=fully Liberalized)",
    "Real long term government bond yield, percent": "Real Long Term Government Bond Yield",
    "Reserve/(Import/12) ": "Reserve/(import/12)",
    "Reserves (Months of Imports) ": "Reserves (months Of Imports)",
    "Reserves/Broad Money": "Reserves/broad Money",
    "Reserves/Short-term Debt (STD)": "Reserves/short-term Debt (std)",
    "Resident Openness Index (1=fully liberalized)": "Resident Openness Index (1=fully Liberalized)",
    "Revenue": "Government Revenue",
    "Terms of Trade (Index, 2010 = 100)": "Terms Of Trade",
    "Total Investment (% of GDP)": "Total Investment",
    "Trade Balance (% of GDP)": "Trade Balance",
    "Unemployment rate": "Unemployment Rate",
}
