import github
import github.PaginatedList
import github.Repository
import github.MainClass
import github.Requester


class SearchPaginatedList(github.PaginatedList.PaginatedList):
    def _fetchNextPage(self):
        headers, data = self._PaginatedList__requester.requestJsonAndCheck(
            "GET",
            self._PaginatedList__nextUrl,
            parameters=self._PaginatedList__nextParams
        )
        data = data.get('items', [])
        self._PaginatedList__nextUrl = None
        if len(data) > 0:
            links = self._PaginatedList__parseLinkHeader(headers)
            if self._reversed:
                if "prev" in links:
                    self._PaginatedList__nextUrl = links["prev"]
            elif "next" in links:
                self._PaginatedList__nextUrl = links["next"]
        self._PaginatedList__nextParams = None

        content = [
            self._PaginatedList__contentClass(self._PaginatedList__requester, headers, element, completed=False)
            for element in data
        ]
        if self._reversed:
            return content[::-1]
        return content


class WtPreviewRequester(github.Requester.Requester):
    def _Requester__requestRaw(self, cnx, verb, url, requestHeaders, input):
        if not requestHeaders:
            requestHeaders = {}
        requestHeaders['Accept'] = 'application/vnd.github.preview'
        return super(WtPreviewRequester, self)._Requester__requestRaw(cnx, verb, url, requestHeaders, input)


class WtGithub(github.Github):
    def __init__(self, login_or_token=None, password=None, base_url=github.MainClass.DEFAULT_BASE_URL, timeout=github.MainClass.DEFAULT_TIMEOUT, client_id=None, client_secret=None, user_agent='PyGithub/Python', per_page=github.MainClass.DEFAULT_PER_PAGE):
        """
        :param login_or_token: string
        :param password: string
        :param base_url: string
        :param timeout: integer
        :param client_id: string
        :param client_secret: string
        :param user_agent: string
        :param per_page: int
        """
        super(WtGithub, self).__init__(login_or_token, password, base_url, timeout,  client_id, client_secret, user_agent, per_page)
        self._previewRequester = WtPreviewRequester(login_or_token, password, base_url, timeout, client_id, client_secret, user_agent, per_page)

    def search_repos(self, q, sort=None, order=None):
        """
        :calls: `GET /search/repositories?q=:q&sort=:sort&order=:order <http://developer.github.com/v3/http://developer.github.com/v3/search/#search-repositories>`_
        :param keyword: string
        :param language: string
        :rtype: :class:`github.PaginatedList.PaginatedList` of :class:`github.Repository.Repository`
        """
        assert isinstance(q, str), q
        url_parameters = {'q': q}
        if sort:
            url_parameters['sort'] = sort
        if order:
            url_parameters['order'] = order

        return SearchPaginatedList(
            github.Repository.Repository,
            self._previewRequester,
            "/search/repositories",
            url_parameters
        )
