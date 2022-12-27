import pandas as pd

# Series & Create Labels => Series는 1차원 배열(Array)이다.
a = [1, 7, 2]
myser = pd.Series(a, index=["x","y","z"])


# DataFrame => DataFrame은 2차원 자료구조이다. ex) 2차원 배열(Array) or Table with rows and columns
# key에 해당하는 value의 길이는 모두 같아야 한다.
dataSet = {
    'cars': ["BMW", "Volvo", "Ford"],
    'passings': [3, 7, 2]
}
mydf = pd.DataFrame(dataSet)

# loc => Locate Row => 특정 행을 가져올 수 있음
print(mydf.loc[[0, 1, 2]])


# Named Indexes => 인덱스의 이름을 정할 수 있음
mydf2= pd.DataFrame(dataSet, index=["day1","day2","day3"])
print(mydf, mydf2)

# Key/Values Objects as Series
calories = {"day1": 420, "day2": 380, "day3": 390}
mycal = pd.Series(calories, index=["day1", "day2"])


#################################################################################

# csv 읽기
# to_string() => 전체 Row 보여줌 
# 그냥 print는 가져오긴 하는데 너무 많은 데이터가 있다면 중간 생략
df = pd.read_csv('sample.csv')  
print(df.to_string())

# info() => data set의 정보를 가져옴 (행, 열, 인덱스, 값 ...)
print(df.info())

# head() => 인자 지정 안하면 처음부터 5개 행 가져옴
# tail() => head()와 마찬가지, 단 마지막부터 ...
print(df.head())

# dataframe to csv
t = df.to_csv("sample3.csv")
print(t)