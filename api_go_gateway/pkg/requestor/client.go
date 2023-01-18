package requestor

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
)

type HTTPRequester struct {
	client http.Client
}

func (h HTTPRequester) BuildRequest(method string, url string, params string, headers http.Header, data io.Reader) *http.Request {
	request, err := http.NewRequest(method, url, data)

	if err != nil {
		log.Fatal(err)
	}
	request.URL.RawQuery = params
	request.Header = headers
	return request
}

func (h HTTPRequester) Request(req *http.Request) *http.Response {
	response, err := h.client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	return response
}

func (h HTTPRequester) DecoderBody(b *http.Response) (*interface{}, error) {
	t := new(interface{})
	err := json.NewDecoder(b.Body).Decode(t)
	if err != nil {
		return nil, err
	}
	return t, nil
}
