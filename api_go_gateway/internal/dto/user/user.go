package user

type User struct {
	Email  string `json:"email,omitempty"`
	UserID int    `json:"id,omitempty"`
}
