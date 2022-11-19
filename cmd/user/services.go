package user

import "github.com/PapaUlito4ka/Symphony/cmd/database"

func GetOrCreateUser(phone string) (User, bool, error) {
	if err := IsPhoneValid(phone); err != nil {
		return User{}, false, err
	}

	user, err := GetUserByPhone(phone)
	created := false
	if err != nil {
		user, err = CreateUser(phone)
		if err != nil {
			return User{}, false, err
		}
		created = true
	}

	return user, created, nil
}

func GetUserByPhone(phone string) (User, error) {
	user := User{}

	query := database.DB.Where("phone = ?", phone).First(&user)
	if query.Error != nil {
		return User{}, query.Error
	}

	return user, nil
}

func CreateUser(phone string) (User, error) {
	user := User{Phone: phone}

	result := database.DB.Create(&user)
	if result.Error == nil {
		return User{}, result.Error
	}

	return user, nil
}

func CreateUserProfile(userId uint, userData UserProfileDto) (UserProfile, error) {
	userProfile := UserProfile{
		UserId:   userId,
		Username: userData.Username,
	}

	result := database.DB.Create(&userProfile)
	if result.Error == nil {
		return UserProfile{}, result.Error
	}

	return userProfile, nil
}
