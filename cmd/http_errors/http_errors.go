package http_errors

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func BadRequestError(c *gin.Context, err error) {
	c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{"detail": err.Error()})
}

func InternalServerError(c *gin.Context, err error) {
	c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{"detail": err.Error()})
}
