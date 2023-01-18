package posts

import (
	"api_go_gateway/internal/dto/user"
	"bytes"
	"encoding/json"
)

type UpdatePost struct {
	Title  string `json:"title"`
	Body   string `json:"body"`
	UserID int    `json:"user_id,omitempty"`
}

func (n *UpdatePost) BindUser(u user.User) {
	n.UserID = u.UserID
}

type NewPost struct {
	Title  string `json:"title"`
	Body   string `json:"body"`
	UserID int    `json:"user_id,omitempty"`
	Email  string `json:"email,omitempty"`
}

func (n *NewPost) BindUser(u user.User) {
	n.UserID = u.UserID
	n.Email = u.Email
}
func ToBuffer(s interface{}) (bytes.Buffer, error) {
	var b bytes.Buffer
	err := json.NewEncoder(&b).Encode(s)
	if err != nil {
		return b, err
	}
	return b, nil
}
