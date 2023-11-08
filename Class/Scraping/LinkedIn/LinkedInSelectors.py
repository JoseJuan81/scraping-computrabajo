class LinkedInSelectors:
    CANDIDATE_APLICATION_TIME = "div.artdeco-entity-lockup__caption.ember-view > div span"
    CANDIDATE_CITY = "li a div.artdeco-entity-lockup__content  div.artdeco-entity-lockup__metadata"
    CANDIDATE_EMAIL = "ul[aria-live] li:nth-child(2) a div span:nth-child(2)"
    CANDIDATE_EXPERIENCE = "div.artdeco-card section ul li div"
    CANDIDATE_IMG = "img.hiring-selectable-entity__entity.evi-image"
    CANDIDATE_MAS_BUTTON = "button.artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom.artdeco-button--muted.artdeco-button--3"
    CANDIDATE_NAME = "div.artdeco-entity-lockup__content div.hiring-people-card__title"
    CANDIDATE_PHONE = "ul[aria-live] li:nth-child(3) div > div span:nth-child(2)"
    CANDIDATE_PROFILE_PAGE = "div.hiring-profile-highlights__see-full-profile a"

    EMAIL_SELECTOR = "input#session_key"
    PASS_SELECTOR = "input#session_password"
    BTN_SELECTOR = "button[data-id='sign-in-form__submit-btn']"

    LIST_OF_CANDIDATES_SELECTOR = "ul li.hiring-applicants__list-item a.ember-view"

    PAGINATION_BUTTONS_SELECTOR = "ul.artdeco-pagination__pages.artdeco-pagination__pages--number li button"
    PAGINATION_CURRENT_SELECTOR = "ul.artdeco-pagination__pages.artdeco-pagination__pages--number li.selected button"