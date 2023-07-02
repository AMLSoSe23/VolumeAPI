import os
import pandas as pd


class DensityDatabase():
    """Density Database searcher object. Food types are expected to be
    in column 1, food densities in column 2."""
    def __init__(self, db_path):
        """Load food density database from file or Google Sheets ID.

        Inputs:
            db_path: Path to database excel file (.xlsx) or Google Sheets ID.
        """
        if os.path.exists(db_path):
            # Read density database from excel file
            self.density_database = pd.read_excel(
                db_path, sheet_name=0, usecols=[0, 1])
        else:
            self.density_database = pd.read_csv('food_volume_estimation\density_lookup\density.csv')
            # Read density database from Google Sheets URL
            # sheet = 'Sheet1'
            # url = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
            #     db_path, sheet)
            # self.density_database = pd.read_csv(url, usecols=[0, 1],
            #                                     header=None)
        # Remove rows with NaN values
        self.density_database.dropna(inplace=True)

    def query(self, food):
        """Search for food density in database.

        Inputs:
            food: Food type to search for.

        Returns:
            db_entry_vals: Array containing the matched food type
            and its density.
        """
        try:
            # Search for matching food in database
            
            # Old method: fuzzy matching
            # match = process.extractOne(food, self.density_database.values[:,0],
            #                            scorer=fuzz.partial_ratio,
            #                            score_cutoff=80)
            # db_entry = (
            #     self.density_database.loc[
            #     self.density_database[
            #     self.density_database.columns[0]] == match[0]])
            # db_entry_vals = db_entry.values
            # return db_entry_vals[0]
            return self.density_database.loc[self.density_database['food'] == food, 'density'].values[0]
        except:
            return ['None', 1.2]