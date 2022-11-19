package common

import (
	"time"
)

type PhotoMixin struct {
	FullPhoto    string `gorm:"->;<-:false"`
	PreviewPhoto string `gorm:"->;<-:false"`
}

type DateTimeMixin struct {
	CreatedAt time.Time `gorm:"autoCreateTime"`
	UpdatedAt time.Time `gorm:"autoUpdateTime"`
}
