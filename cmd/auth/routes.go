package auth

import (
	"errors"
	"net/http"

	"github.com/PapaUlito4ka/Symphony/cmd/http_errors"
	"github.com/PapaUlito4ka/Symphony/cmd/user"
	"github.com/gin-gonic/gin"
)

func SignUp(c *gin.Context) {
	userProfileDto := user.UserProfileDto{}

	if err := c.ShouldBind(&userProfileDto); err != nil {
		http_errors.BadRequestError(c, err)
		return
	}

	jwtData, err := GetJwtData(c)
	if err != nil {
		http_errors.InternalServerError(c, err)
		return
	}

	userProfile, err := user.CreateUserProfile(jwtData.UserID, userProfileDto)
	if err != nil {
		http_errors.BadRequestError(c, err)
		return
	}

	c.JSON(http.StatusCreated, userProfile)
}

func VerifyCode(c *gin.Context) {
	authDto := AuthDto{}

	if err := c.ShouldBind(&authDto); err != nil {
		http_errors.BadRequestError(c, err)
		return
	}

	if err := authDto.IsValid(); err != nil {
		http_errors.BadRequestError(c, err)
		return
	}

	if err := VerifyAuthCode(authDto.Code); err != nil {
		http_errors.BadRequestError(c, err)
		return
	}

	usr, created, err := user.GetOrCreateUser(authDto.Phone)
	if err != nil {
		http_errors.BadRequestError(c, err)
		return
	}

	statusCode := http.StatusOK
	if created {
		statusCode = http.StatusCreated
	}

	accessToken, refreshToken, err := CreateJwtTokens(usr.ID)
	if err != nil {
		http_errors.InternalServerError(c, err)
		return
	}

	c.JSON(statusCode, JwtDto{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
	})
}

func Refresh(c *gin.Context) {
	refreshToken, err := ParseAuthHeader(c.Request)
	if err != nil {
		http_errors.BadRequestError(c, err)
		return
	}

	claims, err := ExtractTokenMetadata(refreshToken)
	if err != nil {
		http_errors.BadRequestError(c, err)
		return
	}

	if claims.IsAccessToken() {
		http_errors.BadRequestError(c, errors.New("refresh token should be passed"))
		return
	}

	accessToken, refreshToken, err := CreateJwtTokens(claims.UserID)
	if err != nil {
		http_errors.InternalServerError(c, err)
	}

	c.JSON(http.StatusCreated, JwtDto{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
	})
}
