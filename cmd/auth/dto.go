package auth

import (
	"github.com/PapaUlito4ka/Symphony/cmd/user"
)

type AuthDto struct {
	Phone string `json:"phone"`
	Code  string `json:"code"`
}

type JwtDto struct {
	AccessToken  string `json:"accessToken"`
	RefreshToken string `json:"refreshToken"`
}

func (ad *AuthDto) IsValid() error {
	return user.IsPhoneValid(ad.Phone)
}
