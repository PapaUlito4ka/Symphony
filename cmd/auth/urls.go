package auth

import (
	"github.com/gin-gonic/gin"
)

func AuthUrls() *gin.Engine {
	r := gin.Default()

	r.POST("verify-code", VerifyCode)
	r.POST("refresh", Refresh)
	r.POST("sign-up", AuthMiddleware, SignUp)

	return r
}
