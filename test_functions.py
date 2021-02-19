import pandas as pd
import functions
#import unittest

df_expected = df = pd.DataFrame([
    "https://eur-lex.europa.eu/legal-content/AUTO/?uri=CELEX:52021M9911",
    "https://eur-lex.europa.eu/legal-content/AUTO/?uri=CELEX:52020M9911",
    "https://eur-lex.europa.eu/legal-content/AUTO/?uri=CELEX:52020M9614(01)"],
    columns=['link']
    )
df_expected.insert(column="CELEX", value=["52021M9911","52020M9911","52020M9614(01)"],loc=1)

def test_celex_separation(df, df_expected):
    df_expected = df_expected["CELEX"]
    df_result = functions.celex_separation(df)["CELEX"]
    assert df_result[1] == df_expected[1]

test_celex_separation(df, df_expected)


# class TestListElements(unittest.TestCase):
#     def setUp(self):
#         self.expected = df_result["CELEX"]
#         self.result = functions.celex_separation(df)["CELEX"]
    
#     def test_list_equal(self):
#         """Will succeed"""
#         self.assertEqual(self.result, self.expected)



# class TestListElements(unittest.TestCase):
#     def setUp(self):
#         self.expected = ['foo', 'bar', 'baz']
#         self.result = ['baz', 'foo', 'bar']

#     def test_count_eq(self):
#         """Will succeed"""
#         self.assertCountEqual(self.result, self.expected)

#     def test_list_eq(self):
#         """Will fail"""
#         self.assertListEqual(self.result, self.expected)


# if __name__ == "__main__":
#     unittest.main()

