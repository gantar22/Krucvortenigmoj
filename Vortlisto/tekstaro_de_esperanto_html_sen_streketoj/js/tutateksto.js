let montru = true;
const div_tekstarteksto = $('div.tekstarteksto');
let dialogo_malfermita = false;
let unika_id = 1;

const FermiDialogon = (dialogo) => {
	dialogo.off().remove();
	dialogo_malfermita = false;
	body.removeClass('dialogo');
};

const Dialogo = (teksto, agoj, finago) => {
	const mia_id = 'dialogo' + unika_id++;
	const dialogo = $(`<div id="${mia_id}" class="dialogo">`);
	const ekstera = $('<div class="ekstera" tabindex="-1">');
	dialogo.data('ekstera', ekstera);
	const ena = $(`<div class="ena">`);
	const kapo = $('<header/>');
	const h2 = $(`<h2>Tekstaro</h2>`);
	const butono_fermi = $('<button class="fermilo fokusebla" title="Fermi">✕</button>');
	const enhavo = $(`<div class="enhavo"/>`);
	if (typeof teksto === 'string') {
		enhavo.text(teksto);
	} else {
		enhavo.append(teksto);
	}
	h2.append(butono_fermi);
	kapo.append(h2);

	ena.append(kapo).append(enhavo);

	let piedo;
	if (agoj && agoj.length) {
		piedo = $('<footer/>');
		agoj.forEach(ago => {
			let butono;
			if (typeof ago === 'string') {
				butono = $('<p class="dialogoteksto"/>').text(ago);
			} else {
				if (ago.hasClass && ago.hasClass('informoj')) {
					piedo.append(ago);
				} else {
					butono = $('<button/>');
					if (typeof ago.teksto === 'string') {
						butono.text(ago.teksto);
					} else {
						butono.append(ago.teksto);
					}
					if (ago.click) {
						butono.addClass('click').data('click', ago.click);
					}
				}
			}
			piedo.append(butono);
		});
		ena.append(piedo);
	} else {
		enhavo.addClass('senbutonoj');
	}

	ekstera.append(ena);
	dialogo.append(ekstera);

	body.append(dialogo).addClass('dialogo');
	const window_width = $(window).width();
	ekstera.css({'width': (window_width) + 'px'});

	dialogo_malfermita = dialogo;

	if (piedo) {
		piedo.find('button').first().focus();
	} else {
		butono_fermi.focus();
	}

	dialogo.on('click', 'button.fermilo, div.ekstera', () => {
		FermiDialogon(dialogo);
		if (finago) {
			finago();
		}
	});
	dialogo.on('keyup', (e) => {
		if (e.which === 27) {
			FermiDialogon(dialogo);
			if (finago) {
				finago();
			}
		}
	});
	dialogo.on('click', 'button.click', (e) => {
		const butono = $(e.currentTarget);
		const click = butono.data('click');
		if (typeof click === 'function') {
			click();
		}
		if (finago) {
			finago();
		}
		FermiDialogon(dialogo);
	});
};
var URLParametroj = new URLSearchParams(window.location.search);
const t_kontrolado = URLParametroj.get('t_kontrolado')
const ref_n = URLParametroj.get('ref_n')
var la_sekcio = URLParametroj.get('sekcio');
const PreniIdonPorPIV = async obj => {
	if (obj.hasClass('editoral')) {
		return;
	}
	// Preni la alinean id-atributon por uzo en la PIV-redaktejo
	let id = obj.prop('id');
	if (id) {
		if (la_sekcio) {
			id += '_' + la_sekcio;
		}
		const memorteksto = ' t="' + id  + '"';
		if (navigator.clipboard) {
			try {
				await navigator.clipboard.writeText(memorteksto);
				Dialogo($('<p>Kopiis: <strong>' + memorteksto + '</strong></p>'));
			} catch (err) {
				Dialogo('La kopiado malsukcesis. Bv. provi denove.');
			}
		} else {
			Dialogo($('<p>La aŭtomata kopiado ne sukcesis. Bv. noti la jenan tekston:<br/><strong>' + memorteksto + '</strong></p>'));
		}
	}
};
div_tekstarteksto.on('click', '*[id]', evento => {
	if (evento.altKey) {
		PreniIdonPorPIV($(evento.currentTarget));
		return false;
	}
});
const body = $('body');
const qs = key => {
	key = key.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
	const match = location.search.match(new RegExp("[?&]"+key+"=([^&]+)(&|$)"));
	return match && decodeURIComponent(match[1].replace(/\+/g, " "));
};
const aktuala_sekcio = $('#aktuala_sekcio');
if (aktuala_sekcio.length) {
	if (qs('tuj') === '1') {
		montru = false;
		aktuala_sekcio[0].click();
		return;
	}
	const alantaua = qs('alantaua');
	let ligilo;
	if (alantaua) {
		const antaua = aktuala_sekcio.closest('li').prev();
		if (antaua.length) {
			ligilo = antaua.find('a');
		}
	} else {
		const alposta = qs('alposta');
		if (alposta) {
			const posta = aktuala_sekcio.closest('li').next();
			if (posta.length) {
				ligilo = posta.find('a');
			}
		}
	}
	if (ligilo && ligilo.length) {
		const href = ligilo.attr('href');
		if (href) {
			montru = false;
			window.location = href;
		}
	} else {
		const al_aktuala_sekcio = $('#alaktualasekcio');
		if (al_aktuala_sekcio.length) {
			const sekcio_button = $('<button/>');
			const sekcio_teksto_1 = $('<span/>').text('Montri la aktualan sekcion de la teksto:');
			const sekcio_teksto_2 = $('<span class="titolo"/>').text('“' + aktuala_sekcio.text() + '”');
			sekcio_button.append(sekcio_teksto_1).append(sekcio_teksto_2);
			al_aktuala_sekcio.append(sekcio_button);
			sekcio_button.on('click', () => aktuala_sekcio[0].scrollIntoView());
		}
	}
} else {
	div_tekstarteksto.find('span.trafo').each( (index, obj) => {
		const trafo = $(obj);
		trafo.html(trafo.html().replace(/^ /, '<span class="trafospaceto"> </span>').replace(/ $/, '<span class="trafospaceto"> </span>'));
	});
}

// Ligiloj en Sinjoro Tadeo al alia sekcio
body.on('click', 'a', (e) => {
	var target = e.currentTarget
	const hash = target.hash
	if (hash.match(/sinjoro-tadeo/)) {
		let href = target.href
		const sekcio = href.match(/sekcio=sinjoro-tadeo-(\d+)/)
		if (sekcio && sekcio[1]) {
			const target_sekcio = hash.match(/sinjoro-tadeo-(\d+)-/)
			if (sekcio[1] !== target_sekcio[1]) {
				href = href.replace(/&sekcio=sinjoro-tadeo-\d+/, '&sekcio=sinjoro-tadeo-' + target_sekcio[1])
				window.location = href
			}
		}
	}
});

if (montru) {
	body.removeClass('kashita');
	const hash = window.location.hash;
	const uzas_streketojn = document.querySelector('div.tekstarteksto span.streketo');
	const trafo = $('span.trafo');
	const hash_loko = $(hash);
	const sagujo = $('<div id="sagujo">');
	const sagoj = $('<span id="sagoj" class="butono">');
	const streketoj = $('<span class="sago streketoj" title="Kaŝi streketojn">').text('●');
	const suprensago = $('<span class="sago supren" title="Al la komenco de la teksto">').text('⇑');
	sagoj.append(suprensago);
	if (hash_loko.length) {
		const trafosago = $('<span class="sago trafosago" title="Al la alineo kun serĉotrafo">').text('◎');
		sagoj.append(trafosago);
	}
	const subensago = $('<span class="sago suben" title="Al la fino de la teksto">').text('⇓');
	sagoj.append(subensago);
	if (uzas_streketojn) {
		sagoj.append(streketoj);
	}
	sagujo.append(sagoj);
	body.prepend(sagujo);
	sagujo.on('click', 'span.sago.supren', () => $(window).scrollTop(0));
	if (hash_loko.length) {
		sagujo.on('click', 'span.sago.trafosago', () => hash_loko[0].scrollIntoView());
	}
	sagujo.on('click', 'span.sago.suben', () => $('br.rompo').last()[0].scrollIntoView());
	if (uzas_streketojn) {
		sagujo.on('click', 'span.sago.streketoj', () => {
			if (div_tekstarteksto.hasClass('kashi_streketojn')) {
				div_tekstarteksto.removeClass('kashi_streketojn');
				streketoj.attr('title', 'Kaŝi streketojn');
			} else {
				div_tekstarteksto.addClass('kashi_streketojn');
				streketoj.attr('title', 'Malkaŝi streketojn');
			}
		});
	}
	if (hash_loko.length) {
		setTimeout( () => {
			hash_loko.addClass('celita');
			if (trafo.length) {
				trafo[0].scrollIntoView();
			} else {
				hash_loko[0].scrollIntoView();
			}
		}, 100);
	}
	if (t_kontrolado) {
		const trafoj = div_tekstarteksto.find('span.trafo')
		const respondo = {'ref_n': ref_n, 'trafoj': trafoj.length}
		if (LOKA) {
			window.opener.postMessage(respondo, 'https://redaktejo.vortaro.loka')
		} else {
			window.opener.postMessage(respondo, 'https://redaktejo.vortaro.net')
		}
		window.close()
	}
}
