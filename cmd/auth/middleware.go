package auth

import (
	"github.com/PapaUlito4ka/Symphony/cmd/http_errors"
	"github.com/gin-gonic/gin"
)

func AuthMiddleware(c *gin.Context) {
	jwtData, err := ParseJwtToken(c.Request)
	if err != nil {
		http_errors.BadRequestError(c, err)
		return
	}
	c.Set("auth", jwtData)

	c.Next()
}
