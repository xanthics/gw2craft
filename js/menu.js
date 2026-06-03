/* From: http://www.kriesi.at/archives/create-a-multilevel-dropdown-menu-with-css-and-improve-it-via-jquery */

function mainmenu(){
/*$("nav ul").css({display: "none"}); // Opera Fix*/
    $("nav li").hover(function(){
		$(this).find('ul:first').css({visibility: "visible",display: "none"}).show(200);
		},function(){
		$(this).find('ul:first').css({visibility: "hidden"});
		});
}

/* From: http://www.codeography.com/2012/10/11/convert-timestamps-localtime-jquery.html */

(function() {
  (function($) {
    return $.fn.localtime = function() {
      var fmtDate, fmtZero;
      fmtZero = function(str) {
        return ('0' + str).slice(-2);
      };
      fmtDate = function(d) {
        var hour, meridiem;
        hour = d.getHours();
        if (hour < 12) {
          meridiem = "AM";
        } else {
          meridiem = "PM";
        }
        if (hour === 0) { hour = 12; }
        if (hour > 12) { hour = hour - 12; }
        return hour + ":" + fmtZero(d.getMinutes()) + " " + meridiem + " " + (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
      };
      return this.each(function() {
        var tagText;
        tagText = $(this).html();
        $(this).html(fmtDate(new Date(tagText)));
        return $(this).attr("title", tagText);
      });
    };
  })(jQuery);
}).call(this);

$(document).ready(function(){					
	mainmenu();
	$("span.localtime").localtime();
	// Apply any browser-restored start-level value + have-input values on load.
	if (document.getElementById('start-level')) setStartLevel();
});

function updateNeed(field, val, idval) {
    field.setAttribute('data-manual', '1');
    recomputeItem(field.getAttribute('data-item'));
    updateRemaining();
}

function updateBank(api_key) {
    var dict = {}
    var done = 2

    $(['materials', 'bank']).each(function() {
        var endpoint = this;
        $.getJSON('https://api.guildwars2.com/v2/account/' + endpoint + '?access_token=' + api_key, function(data) {
            //for item in data
            $.each(data, function(value) {
                if(data[value]) {
                    var exists = dict[data[value].id];
                    if(!exists) {
                        dict[data[value].id] = 0;
                    }
                    dict[data[value].id] += data[value].count
                }
            });
            done -= 1
            if (done == 0) {

                for (var key in dict) {
                    if (dict.hasOwnProperty(key)) {
                        var input = document.querySelector('input[data-item="' + key + '"]') || document.getElementById(key + 'ih');
                        if (input && input.getAttribute('data-manual') !== '1') {
                            input.value = dict[key];
                            var iid = input.getAttribute('data-item');
                            if (iid) {
                                recomputeItem(iid);
                            } else {
                                input.oninput();
                            }
                        }
                    }
                }
                updateRemaining();
            }
        });
    });
	$.getJSON('https://api.guildwars2.com/v2/account/recipes?access_token=' + api_key, function(data) {
		//for item in data
		$.each(data, function(value) {
			var reci = data[value]
			if($("#reci" + reci).length) {
				$("#reci" + reci).prop('checked', true);
			}
		});
	});
}

function updateRemaining() {
    var sum = 0;
    var copper = 0;
    var silver = 0;
    var gold = 0;
    var temp = 0;

    $(".vTotal").each(function(){
        temp = +$(this).val() * +$(this).attr("raw_copper");
        if(temp > 0) {
            sum += temp;
        }
    });
    copper = sum % 100;
    sum = Math.floor(sum / 100);
    silver = sum % 100;
    sum = Math.floor(sum / 100);
    gold = sum;

    celements = document.getElementsByClassName("mycopper");
    selements = document.getElementsByClassName("mysilver");
    gelements = document.getElementsByClassName("mygold");

    for(var i=0; i<celements.length; i++) {
        celements[i].textContent=("00" + copper).slice(-2);
    }
    for(var i=0; i<selements.length; i++) {
        selements[i].textContent=("00" + silver).slice(-2);
    }
    for(var i=0; i<gelements.length; i++) {
        gelements[i].textContent=gold.toString();
    }
}


// Recomputes the top-level "Need" cell for one item based on currently visible
// tier-buy rows, then redistributes the item's "have" value into those rows.
// Items with no tier-buy presence (karma, recipes, mixed-only) keep their
// original need; visibility changes only affect items broken into tier rows.
function recomputeItem(itemId) {
    if (!itemId) return;
    var haveInput = document.querySelector('input[data-item="' + itemId + '"]');
    var have = haveInput ? (+haveInput.value || 0) : 0;
    var origNeed = haveInput ? (+haveInput.getAttribute('data-original-need') || 0) : 0;

    var tierRows = document.querySelectorAll('.tierbuy-row[data-item="' + itemId + '"]');
    var visibleNeed = origNeed;
    if (tierRows.length > 0) {
        visibleNeed = 0;
        for (var r = 0; r < tierRows.length; r++) {
            var container = tierRows[r].parentNode;
            var hidden = container && container.classList && container.classList.contains('tier-skip');
            if (!hidden) {
                visibleNeed += +tierRows[r].getAttribute('data-original-need') || 0;
            }
        }
    }

    var needCell = document.getElementById(itemId + 'bv');
    if (needCell) {
        var rem = Math.max(0, visibleNeed - have);
        needCell.value = rem;
        needCell.setAttribute('data-need', rem > 0 ? 'more' : 'done');
    }

    redistributeItem(itemId);
}

// Distributes the "have" value for one item across visible per-tier buy rows.
// Fills earliest visible tier first; skipped (hidden) tiers don't consume.
function redistributeItem(itemId) {
    if (!itemId) return;
    var haveInputs = document.querySelectorAll('input[data-item="' + itemId + '"]');
    var pool = 0;
    for (var i = 0; i < haveInputs.length; i++) {
        pool += +haveInputs[i].value || 0;
    }

    var rows = document.querySelectorAll('.tierbuy-row[data-item="' + itemId + '"]');
    var sorted = Array.prototype.slice.call(rows).sort(function(a, b) {
        return +a.getAttribute('data-tier') - +b.getAttribute('data-tier');
    });
    var affectedTiers = {};
    for (var j = 0; j < sorted.length; j++) {
        var row = sorted[j];
        var tier = row.getAttribute('data-tier');
        var orig = +row.getAttribute('data-original-need') || 0;
        var container = row.parentNode;
        var hidden = container && container.classList && container.classList.contains('tier-skip');
        var allocate = hidden ? 0 : Math.min(pool, orig);
        if (!hidden) pool -= allocate;
        var remaining = orig - allocate;
        var qty = row.querySelector('span.quantity');
        if (qty) {
            qty.textContent = remaining;
            qty.setAttribute('data-need', remaining > 0 ? 'more' : 'done');
        }
        affectedTiers[tier] = true;
    }

    for (var t in affectedTiers) {
        if (affectedTiers.hasOwnProperty(t)) recomputeTierCost(t);
    }
    recomputeRollingTotals();
}

// Recomputes the total cost for one tier from its row remainders.
function recomputeTierCost(tier) {
    var rows = document.querySelectorAll('.tierbuy-row[data-tier="' + tier + '"]');
    var total = 0;
    for (var i = 0; i < rows.length; i++) {
        var qty = rows[i].querySelector('span.quantity');
        var remaining = qty ? (+qty.textContent || 0) : 0;
        var rawCopper = +rows[i].getAttribute('data-raw-copper') || 0;
        total += remaining * rawCopper;
    }
    var costSpan = document.querySelector('.tier-cost[data-tier="' + tier + '"]');
    if (costSpan) {
        costSpan.setAttribute('data-raw-copper', total);
        costSpan.innerHTML = formatCopper(total);
    }
}

// Recomputes rolling cumulative totals for all visible tiers, in tier order.
function recomputeRollingTotals() {
    var costs = document.querySelectorAll('.tier-cost');
    var sorted = Array.prototype.slice.call(costs).sort(function(a, b) {
        return +a.getAttribute('data-tier') - +b.getAttribute('data-tier');
    });
    var rolling = 0;
    for (var i = 0; i < sorted.length; i++) {
        var tier = sorted[i].getAttribute('data-tier');
        var header = sorted[i].parentNode;
        var headerHidden = header && header.classList && header.classList.contains('tier-skip');
        if (!headerHidden) rolling += +sorted[i].getAttribute('data-raw-copper') || 0;
        var rollSpan = document.querySelector('.tier-rolling[data-tier="' + tier + '"]');
        if (rollSpan) {
            rollSpan.setAttribute('data-raw-copper', rolling);
            rollSpan.innerHTML = formatCopper(rolling);
        }
    }
}

// Formats a copper amount with the same gold/silver/copper icon spans Python emits.
function formatCopper(c) {
    c = Math.max(0, parseInt(c, 10) || 0);
    function pad2(n) { return n < 10 ? '0' + n : '' + n; }
    var copper = c % 100;
    var rest = Math.floor(c / 100);
    var silver = rest % 100;
    var gold = Math.floor(rest / 100);
    if (c >= 10000) {
        return gold + '<span class="goldIcon"></span>' +
               pad2(silver) + '<span class="silverIcon"></span>' +
               pad2(copper) + '<span class="copperIcon"></span>';
    }
    if (c >= 100) {
        return silver + '<span class="silverIcon"></span>' +
               pad2(copper) + '<span class="copperIcon"></span>';
    }
    return c + '<span class="copperIcon"></span>';
}

// Toggles visibility of per-tier and per-level blocks based on the start-level input,
// then re-flows bank inventory into newly-visible tiers.
function setStartLevel() {
    var input = document.getElementById('start-level');
    if (!input) return;
    var level = +input.value || 0;

    // Show a warning when start-level is mid-tier (on guides that have tier-buy lists).
    // Tier boundaries: 0, 75, 150, 225, 300. Past 400 the final tier is also fully done.
    var warningEl = document.getElementById('start-level-warning');
    if (warningEl) {
        var hasTierBuys = document.querySelectorAll('.tierbuy-row').length > 0;
        var atBoundary = (level === 0 || level === 75 || level === 150 ||
                          level === 225 || level === 300 || level >= 400);
        warningEl.style.display = (hasTierBuys && !atBoundary) ? 'inline' : 'none';
    }

    var tierEls = document.querySelectorAll('[data-tier]');
    for (var i = 0; i < tierEls.length; i++) {
        var t = +tierEls[i].getAttribute('data-tier');
        var span = (t === 300) ? 100 : 75;
        if (level >= t + span) {
            tierEls[i].classList.add('tier-skip');
        } else {
            tierEls[i].classList.remove('tier-skip');
        }
    }

    var levelEls = document.querySelectorAll('.level-block');
    for (var j = 0; j < levelEls.length; j++) {
        var l = +levelEls[j].getAttribute('data-level');
        if (level >= l + 25) {
            levelEls[j].classList.add('level-skip');
        } else {
            levelEls[j].classList.remove('level-skip');
        }
    }

    var seen = {};
    var haves = document.querySelectorAll('input[data-item][data-original-need]');
    for (var k = 0; k < haves.length; k++) {
        var id = haves[k].getAttribute('data-item');
        if (!seen[id]) {
            seen[id] = true;
            recomputeItem(id);
        }
    }
    updateRemaining();
}
