package middlewares

import (
	"api_go_gateway/internal/dto/user"
	"api_go_gateway/pkg/requestor"
	"bytes"
	"github.com/gin-gonic/gin"
	"github.com/goccy/go-json"
	"io"
	"log"
	"strings"
)

func AuthMiddleware(URL string) gin.HandlerFunc {
	return func(c *gin.Context) {
		authHeader := strings.Fields(c.GetHeader("Authorization"))
		if len(authHeader) <= 1 {
			c.JSON(403, gin.H{"detail": "Not authenticated"})
			c.Abort()
			return
		}
		token := new(bytes.Buffer)
		err := json.NewEncoder(token).Encode(map[string]string{"access_token": authHeader[1]})

		if err != nil {
			c.JSON(500, gin.H{"detail": "auth internal error"})
			c.Abort()
			return
		}

		url := URL + "/check_token"
		var client requestor.HTTPRequester

		req := client.BuildRequest("POST", url, "", nil, token)
		r := client.Request(req)
		defer r.Body.Close()

		if r.StatusCode != 200 {
			c.DataFromReader(r.StatusCode, r.ContentLength, r.Header.Get("Content-Type"), r.Body, nil)
			c.Abort()
			return
		}
		body, err := io.ReadAll(r.Body)
		var u user.User
		if err != nil {
			log.Fatal(err)
		}
		err = json.Unmarshal(body, &u)
		if err != nil {
			log.Fatal(err)
		}
		c.Set("user", u)
	}
}
