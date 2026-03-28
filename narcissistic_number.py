def is_narcissistic_number(num):
    """
    判断一个数是否为水仙花数
    
    水仙花数是指一个n位数，其各位数字的n次方和等于该数本身
    
    Args:
        num: 要判断的整数
    
    Returns:
        bool: 如果是水仙花数返回True，否则返回False
    """
    # 确保输入是正整数
    if not isinstance(num, int) or num < 0:
        return False
    
    # 将数字转换为字符串，以便获取位数和各位数字
    num_str = str(num)
    n = len(num_str)
    
    # 计算各位数字的n次方和
    sum_of_powers = sum(int(digit) ** n for digit in num_str)
    
    # 判断是否等于原数
    return sum_of_powers == num

def user_interaction():
    """
    用户交互界面
    """
    print("欢迎使用水仙花数判断程序！")
    print("水仙花数是指一个n位数，其各位数字的n次方和等于该数本身。")
    print("例如：153 = 1³ + 5³ + 3³ = 1 + 125 + 27 = 153")
    print("=" * 50)
    
    while True:
        user_input = input("请输入一个整数（输入'q'或'quit'退出程序）：")
        
        # 检查是否退出程序
        if user_input.lower() in ['q', 'quit']:
            print("感谢使用，再见！")
            break
        
        try:
            # 尝试将输入转换为整数
            num = int(user_input)
            
            if is_narcissistic_number(num):
                print(f"✓ {num} 是水仙花数")
            else:
                print(f"✗ {num} 不是水仙花数")
            
            # 显示计算过程
            num_str = str(num)
            n = len(num_str)
            if n > 1:
                process = " + ".join([f"{digit}^{n}" for digit in num_str])
                result = sum(int(digit) ** n for digit in num_str)
                print(f"计算过程：{num} = {process} = {result}")
            
        except ValueError:
            print("❌ 输入错误，请输入一个有效的整数！")
        
        print("=" * 50)

# 示例用法
if __name__ == "__main__":
    # 测试一些数字
    test_numbers = [153, 370, 371, 407, 1634, 8208, 9474, 123, 456, 789]
    print("===== 水仙花数测试示例 =====")
    for num in test_numbers:
        if is_narcissistic_number(num):
            print(f"{num} 是水仙花数")
        else:
            print(f"{num} 不是水仙花数")
    print("==========================")
    
    # 启动用户交互
    user_interaction()