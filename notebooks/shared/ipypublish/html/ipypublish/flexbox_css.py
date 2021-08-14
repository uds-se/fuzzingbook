tpl_dict = {

    'meta_docstring': r""" adds flex boxes (https://github.com/Munawwar/flex-helper)  """,

    "html_header": r"""

<style type="text/css">
/*Stack child items vertically*/
.vbox {
    display: flex;

    /*Align children vetically*/
    flex-direction: column;
    align-content: flex-start;

    overflow: hidden; /*Prevent extending beyond boundaries*/
}
/*Stack child items horizontally*/
.hbox {
    display: flex;

    /*Align children horizontally*/
    flex-direction: row;
    align-content: flex-start;

    /*Wrap items to next line on main-axis*/
    flex-wrap: wrap;

    overflow: hidden; /*Prevent extending beyond boundaries*/
}
/*Stretch item along parent's main-axis*/
.flex {
    flex: 1;
}

/*Stretch item along parent's cross-axis Overrides any cross-* class of parent*/
.stretch-self {
    align-self: stretch;
}
/*Center item along parent's cross-axis. Overrides any cross-* class of parent*/
.center-self {
    align-self: center;
}

/*Stack child items to the main-axis start*/
.main-start {
    justify-content: flex-start;
}
/*Stack child items to the cross-axis start*/
.cross-start {
    align-items: flex-start;
    align-content: flex-start;
}
/*Stack child items to the main-axis center*/
.main-center {
    justify-content: center;
}
/*Stack child items to the cross-axis center*/
.cross-center {
    align-items: center;
    align-content: center;
}
/*Stack child items to the main-axis end.*/
.main-end {
    justify-content: flex-end;
}
/*Stack child items to the cross-axis end.*/
.cross-end {
    align-items: flex-end;
    align-content: flex-end;
}
/*Stretch child items along the cross-axis*/
.cross-stretch {
    align-items: stretch;
    align-content: stretch;
}

/*Wrap items to next line on main-axis*/
.wrap {
    flex-wrap: wrap;
}
/*Don't wrap items to next line on main-axis*/
.nowrap {
    flex-wrap: nowrap;
}

</style>
"""

}
