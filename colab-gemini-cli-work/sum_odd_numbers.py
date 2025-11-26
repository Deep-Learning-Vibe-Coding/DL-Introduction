# sum_odd_numbers.py

total_sum = 0
for number in range(1, 101):
    if number % 2 != 0:  # Check if the number is odd
        total_sum += number

print(f"The sum of odd numbers from 1 to 100 is: {total_sum}")
