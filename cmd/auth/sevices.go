package auth

import "errors"

func VerifyAuthCode(code string) error {
	if code != "1234" {
		return errors.New("invalid authentication code")
	}
	return nil
}
