
# works is a list of sentences which are lists of words
import string

from bitlibroj import get_epub_paths, get_clauses
from radikoj import base_word_score, decompose_word, load_roots
from tekstaro import get_tekstaro_sentences, get_tekstaro_paths


def get_all_pairs(works : list[list[str]], roots : dict[str,int]) -> dict[tuple[str,str],int]:

    def score_pairs(pair : tuple[str,str], roots : dict[str,int], score_cache : dict[tuple[str,str],int], appearance_count : dict[tuple[str,str],int]):
        if pair in score_cache:
            appearance_count[pair] = appearance_count.get(pair,0) + 1
        else:
            decomped_0 = decompose_word(pair[0],roots)
            decomped_1 = decompose_word(pair[1],roots)
            if len(decomped_0) == 0:
                return
            if len(decomped_1) == 0:
                return
            scores_0 = [base_word_score(decomp,roots) for decomp in decomped_0]
            scores_1 = [base_word_score(decomp,roots) for decomp in decomped_1]
            score_cache[pair] = (max(scores_0) + max(scores_1)) / 2.0
            appearance_count[pair] = 1

    def get_pairs(sentence : list[str], roots : dict[str,int]) -> set[tuple[str,str]]:

        def is_pair(first_word, second_word, rec = False) -> list[tuple[str,str]]:
            if len(first_word) < 3 or len(second_word) < 3:
                return []
            bad_adjectives = {'mia','ĝia','via','lia','sia','ŝia','ilia','ria','nia','onia','ka','tia'}
            bad_nouns = {'tio','kio'}
            if first_word[-1] == 'a' and second_word[-1] == 'o':
                if first_word not in bad_adjectives and second_word not in bad_nouns:
                    #return [(first_word,second_word)]
                    return [(first_word,second_word),(first_word,second_word[:-1])]
            if first_word[-2:] == 'aj' and second_word[-2:] == 'oj':
                if first_word[:-1] not in bad_adjectives and second_word[:-1] not in bad_nouns:
                    return [(first_word,second_word),]
            if first_word[-2:] == 'an' and second_word[-2:] == 'on':
                if first_word[:-1] not in bad_adjectives and second_word[:-1] not in bad_nouns:
                    #return [(first_word,second_word),(first_word[:-1],second_word[:-1])]
                    return [(first_word[:-1],second_word[:-1])]
            if first_word[-3:] == 'ajn' and second_word[-3:] == 'ojn':
                if first_word[:-2] not in bad_adjectives and second_word[:-2] not in bad_nouns:
                    #return [(first_word,second_word),(first_word[:-1],second_word[:-1]),(first_word[:-2],second_word[:-2])]
                    return [(first_word[:-1],second_word[:-1])]
            pronouns = {'mi','ĝi','vi','li','si','ŝi','ili','ri','ni','oni'}
            if first_word[-1] == 'i' and second_word[-2:] == 'on':
                if first_word not in pronouns and second_word[:-1] not in bad_nouns:
                    return [(first_word,second_word)]
            if first_word[-1] == 'i' and second_word[-3:] == 'ojn':
                if first_word not in pronouns and second_word[:-2] not in bad_nouns:
                    return [(first_word,second_word)]
            verb_endings = {'is','as','os','us'}
            false_verbs = {'ĝis'}
            if first_word[-2:] in verb_endings and second_word[-2:] == 'on':
                if first_word not in false_verbs and second_word[:-1] not in bad_nouns:
                    return [(first_word,second_word),(first_word[:-2] + 'i',second_word)]
            if first_word[-2:] in verb_endings and second_word[-3:] == 'ojn':
                if first_word not in false_verbs and second_word[:-2] not in bad_nouns:
                    return [(first_word,second_word),(first_word[:-2] + 'i',second_word)]
            if first_word[-1] == 'e' and second_word[-1] == 'i':
                if second_word not in false_verbs and second_word not in pronouns:
                    return [(first_word,second_word)]
            verb_endings = {'is','as','os','us'}
            if first_word[-1] == 'e' and second_word[-2:] in verb_endings:
                if second_word not in false_verbs:
                    return [(first_word,second_word),(first_word,second_word[:-2] + 'i')]
            
            if rec:
                return is_pair(second_word,first_word,False)
            return []

        pairs = set()
        for i in range(len(sentence) - 1):
            for pair in is_pair(sentence[i],sentence[i+1]):
                pairs.add(pair)

        return pairs

    score_cache = {}
    total_appearance_count = {}
    for work in works:
        appearance_count = {}
        for sentence in work:
            pairs = get_pairs(sentence.split(),roots)
            for pair in pairs:
                score_pairs(pair,roots,score_cache,appearance_count)
        for pair in appearance_count.keys():
            total_appearance_count[pair] = total_appearance_count.get(pair,0) + 1
    
    words_too_rare = set()
    for key in score_cache.keys():
        if total_appearance_count.get(key,0) < 2:
            words_too_rare.add(key)
    
    for key in words_too_rare:
        score_cache.pop(key)

    return score_cache

if __name__ == "__main__":
    outputfile = open('./artefaktoj/bitlibroj_pairs.dict','w',encoding='utf8')
    roots : dict[str,int] = load_roots()
    works = []
    for path in get_epub_paths():
        sentences = get_clauses(path)
        works.append(sentences)

    for path in get_tekstaro_paths():
        sentences = get_tekstaro_sentences(path)
        works.append(sentences)

    scores = get_all_pairs(works,roots)

    for pair in scores.keys():
        outputfile.write(f'{pair[0] + pair[1]};{int(scores[pair])}\n')