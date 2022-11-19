package auth

import (
	"errors"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/PapaUlito4ka/Symphony/cmd/constants"
	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v4"
)

type Claims struct {
	jwt.RegisteredClaims
	UserID      uint `json:"userId"`
	AccessToken bool `json:"accessToken"`
}

func (c *Claims) IsAccessToken() bool {
	return c.AccessToken
}

func ParseAuthHeader(r *http.Request) (string, error) {
	authHeader := r.Header.Get("Authorization")
	if authHeader == "" {
		return "", errors.New("authorization header wasn't provided")
	}
	bearerAuth := strings.Split(authHeader, " ")
	if len(bearerAuth) != 2 {
		return "", errors.New("incorrect authorization header")
	}
	if bearerAuth[0] != "Bearer" {
		return "", errors.New("not bearer authorization")
	}

	token := bearerAuth[1]
	return token, nil
}

func VerifyToken(rawToken string) (*jwt.Token, error) {
	token, err := jwt.Parse(rawToken, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return constants.JWT_SECRET, nil
	})
	if err != nil {
		return nil, err
	}
	return token, nil
}

func TokenValid(token *jwt.Token) (jwt.MapClaims, error) {
	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok || !token.Valid {
		return nil, errors.New("map claims parse error")
	}
	return claims, nil
}

func ExtractTokenMetadata(rawToken string) (*Claims, error) {
	token, err := VerifyToken(rawToken)
	if err != nil {
		return nil, err
	}

	claims, err := TokenValid(token)
	if err != nil {
		return nil, err
	}

	userId, ok := claims["userId"].(uint)
	if !ok {
		return nil, errors.New("jwt userID parse error")
	}
	accessToken, ok := claims["accessToken"].(bool)
	if !ok {
		return nil, errors.New("jwt accessToken parse error")
	}

	return &Claims{
		AccessToken: accessToken,
		UserID:      userId,
	}, nil
}

func CreateJwtToken(userID uint, accessToken bool) (string, error) {
	duration := time.Hour * time.Duration(24*7)
	if accessToken {
		duration = time.Minute * time.Duration(15)
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, &Claims{
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(duration)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
		},
		UserID:      userID,
		AccessToken: accessToken,
	})

	tokenString, err := token.SignedString(constants.JWT_SECRET)
	if err != nil {
		return "", err
	}

	return tokenString, nil
}

func CreateJwtTokens(userID uint) (string, string, error) {
	accessTokenString, err := CreateJwtToken(userID, true)
	if err != nil {
		return "", "", err
	}
	refreshTokenString, err := CreateJwtToken(userID, false)
	if err != nil {
		return "", "", err
	}

	return accessTokenString, refreshTokenString, nil
}

func ParseJwtToken(req *http.Request) (*Claims, error) {
	refreshToken, err := ParseAuthHeader(req)
	if err != nil {
		return nil, err
	}

	claims, err := ExtractTokenMetadata(refreshToken)
	if err != nil {
		return nil, err
	}

	if !claims.IsAccessToken() {
		return nil, err
	}

	return claims, nil
}

func GetJwtData(c *gin.Context) (*Claims, error) {
	jwtRawData, exists := c.Get("jwt")
	if !exists {
		return nil, errors.New("jwt key error")
	}
	jwtData, ok := jwtRawData.(*Claims)
	if !ok {
		return nil, errors.New("jwt parse error")
	}

	return jwtData, nil
}
