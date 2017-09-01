(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
class EpisodeComponent extends React.Component {
    render() {
        return React.createElement("div", null, React.createElement("h3", null, " ",  this.props.episode['title'] ), 
            React.createElement("ul", null, 
                 this.props.episode['trivia'].map( function(t) { return React.createElement("li", null,  t['fact'] ) }) 
            )
            )
    }
}

class SeasonComponent extends React.Component {
    render() {
        return  React.createElement("div", null, 
                React.createElement("h2", null, "Season ",  this.props.season['number'] ), 
                 this.props.season['episodes'].map( function(e) { return React.createElement(EpisodeComponent, {episode:  e['episode'] }) }) 
                )
    }
}
var TVTriviaSearch = React.createClass({displayName: "TVTriviaSearch",
  getInitialState: function(){
    return {
    titleInput: '',
    seasonInput: '',
    showData: ''};
  },
  handleSubmit: function(event){
    var searchClass = this;
    var query_string =  "title=" + this.state.titleInput +
                        (this.state.seasonInput ? ("&season=" + this.state.seasonInput) : "") +
                        (this.state.yearInput ? ("&year=" + this.state.yearInput) : "");
    $.ajax({
        url: "/show?" + query_string,
        dataType: 'json',
        beforeSend: function (){
            $('.status').text('Loading...');
        },
        complete: function() {
            $('.status').text('');
        },
        success: function(data) {
            searchClass.setState({ showData:data });
        }
    });
    event.preventDefault();
  },
  handleTitleChange: function(event){
    this.setState({ titleInput: event.target.value })
  },
  handleYearChange: function(event){
    this.setState({ yearInput: event.target.value })
  },
  handleSeasonChange: function(event){
    this.setState({ seasonInput: event.target.value })
  },
  render: function() {
    var season_list_data = [];
    var showData =  this.state.showData['show']
    var title = "";

    if(showData) {
        season_list_data = showData['seasons'];
        title = showData['title'] + " (" + showData['year_start'] + "-" + showData['year_end'] + ")";
    }
    return (
        React.createElement("div", null, 
            React.createElement("form", {onSubmit: this.handleSubmit}, 
                React.createElement("div", {className: "form_container"}, 
                    React.createElement("div", {className: "start_at_container"}, 
                        React.createElement("div", {className: "form_input"}, 
                            React.createElement("label", {for: "title"}, "Title: "), React.createElement("br", null), 
                            React.createElement("input", {idName: "title", type: "text", value: this.state.titleInput, onChange: this.handleTitleChange})
                        ), 
                        React.createElement("div", {className: "form_input"}, 
                            React.createElement("label", {for: "year"}, "Year: "), React.createElement("br", null), 
                            React.createElement("input", {idName: "year", className: "small_input", type: "number", label: "Year", value: this.state.yearInput, onChange: this.handleYearChange}), React.createElement("br", null)
                        ), 
                        React.createElement("div", {className: "form_input"}, 
                            React.createElement("label", {for: "season"}, "Season: "), React.createElement("br", null), 
                            React.createElement("input", {idName: "season", className: "small_input", type: "text", label: "Season", placeholder: "1", value: this.state.seasonInput, onChange: this.handleSeasonChange})
                        ), 
                        React.createElement("div", {className: "form_input"}, 
                            React.createElement("div", {className: "status"})
                        )
                    ), React.createElement("br", null), 
                    React.createElement("div", {className: "form_input"}, 
                        React.createElement("input", {type: "submit", value: "Search"}), React.createElement("br", null)
                    )
                )
            ), 
           React.createElement("div", {className: "trivia_container"}, 
                React.createElement("h1", null, " ",  title, " "), 
                 season_list_data.map(function(s) { return React.createElement(SeasonComponent, {season:  s['season'] }) }) 
           )
        )
    )
  }

});

ReactDOM.render(
  React.createElement(TVTriviaSearch, null),
  document.getElementById('content')
);

},{}]},{},[1]);
