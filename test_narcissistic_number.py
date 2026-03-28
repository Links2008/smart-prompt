import unittest
from narcissistic_number import is_narcissistic_number

class TestNarcissisticNumber(unittest.TestCase):
    """测试水仙花数字判断函数"""
    
    def test_known_narcissistic_numbers(self):
        """测试已知的水仙花数"""
        # 3位水仙花数
        self.assertTrue(is_narcissistic_number(153))
        self.assertTrue(is_narcissistic_number(370))
        self.assertTrue(is_narcissistic_number(371))
        self.assertTrue(is_narcissistic_number(407))
        
        # 4位水仙花数
        self.assertTrue(is_narcissistic_number(1634))
        self.assertTrue(is_narcissistic_number(8208))
        self.assertTrue(is_narcissistic_number(9474))
        
        # 5位水仙花数
        self.assertTrue(is_narcissistic_number(54748))
        self.assertTrue(is_narcissistic_number(92727))
        self.assertTrue(is_narcissistic_number(93084))
        
        # 1位数字都是水仙花数
        for i in range(10):
            self.assertTrue(is_narcissistic_number(i))
    
    def test_non_narcissistic_numbers(self):
        """测试不是水仙花数的数字"""
        # 普通数字
        self.assertFalse(is_narcissistic_number(123))
        self.assertFalse(is_narcissistic_number(456))
        self.assertFalse(is_narcissistic_number(789))
        
        # 接近水仙花数的数字
        self.assertFalse(is_narcissistic_number(154))  # 153+1
        self.assertFalse(is_narcissistic_number(372))  # 371+1
        self.assertFalse(is_narcissistic_number(1633))  # 1634-1
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 0是水仙花数
        self.assertTrue(is_narcissistic_number(0))
        
        # 负数不是水仙花数
        self.assertFalse(is_narcissistic_number(-153))
        self.assertFalse(is_narcissistic_number(-1))

if __name__ == "__main__":
    unittest.main()