import csv
import unittest

from pr_res import pr_res


class TestRegEx(unittest.TestCase):
    def test_reg_ex(self):
        with open('pr_res_cases.csv') as file:
            csv_file = csv.reader(file.read().splitlines())
            for row in csv_file:
                if row[0] == 'pr' and row[1] == 'title':
                    continue
                print('row', row)
                self.check_reg_ex(row)

    def check_reg_ex(self, row):
        title, expected = row[1], row[2]
        for i, re_module in enumerate(pr_res):
            match = re_module.search(title)
            if match:
                break
        if expected:
            self.assertIsNotNone(match)
            self.assertEqual(match.groups()[-1], expected)
        else:
            self.assertIsNone(match)


if __name__ == "__main__":
    print('Starting test')
    unittest.main()
