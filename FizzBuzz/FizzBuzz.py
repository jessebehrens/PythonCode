#I just learned about FizzBuzz so I thought I would solve it!
#Please provide any feedback on how I could speed this up

#Put in the upper range, Python will handle the +1
upperbound=100


#Print the value for i unless:
  # - if i is divisible by 3 then print Fizz
  # - if i is divisible by 5 then print Buzz
  # - if both then print FizzBuzz
    
for i in range(1, upperbound+1):
    output=str()
    if i % 3 == 0 or i % 5 ==0:
        if i % 3 == 0:
            output +='Fizz'
        if i % 5 == 0:
            output +='Buzz'
    else:
        output=i

    print(output)
