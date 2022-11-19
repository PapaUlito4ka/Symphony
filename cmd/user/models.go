package user

import "github.com/PapaUlito4ka/Symphony/cmd/common"

type User struct {
	ID       uint
	Phone    string
	IsActive bool `gorm:"default:true"`
}

type UserProfile struct {
	UserId   uint
	Username string
	Dates    common.DateTimeMixin `gorm:"embedded"`
	Photos   common.PhotoMixin    `gorm:"embedded"`
}

func (User) TableName() string {
	return "user"
}

func (UserProfile) TableName() string {
	return "user_profile"
}
