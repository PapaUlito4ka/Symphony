package user

import (
	"errors"

	"github.com/dongri/phonenumber"
)

func IsPhoneValid(phone string) error {
	if phonenumber.ParseWithLandLine(phone, "RU") == "" {
		return errors.New("phone parse error")
	}
	return nil
}
