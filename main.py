# 0. 클라이언트마다 데이터베이스(=db) 따로 생성
# 1. 서버에서 데이터 받아옴
# 2. 클라이언트 식별번호로 mysql connection 생성
# 3. 해당 connection의 커서 생성
# 4. 받아온 데이터 Insert
# 5. 저장한 데이터 Select
# 6. pandas를 이용해서 테이블 화(into DataFrame)시킨다.
# 7. 테이블 화 시킨 데이터들(= DataFrame)을 csv로 변환(into csv)