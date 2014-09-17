IGNORE_WORDS = frozenset([
 'a', 'about', 'according', 'accordingly', 'affected', 'affecting', 'after',
 'again', 'against', 'all', 'almost', 'already', 'also', 'although',
 'always', 'am', 'among', 'an', 'and', 'any', 'anyone', 'apparently', 'are',
 'arise', 'as', 'aside', 'at', 'away', 'be', 'became', 'because', 'become',
 'becomes', 'been', 'before', 'being', 'between', 'both', 'briefly', 'but',
 'by', 'came', 'can', 'cannot', 'certain', 'certainly', 'could', 'did', 'do',
 'does', 'done', 'during', 'each', 'either', 'else', 'etc', 'ever', 'every',
 'following', 'for', 'found', 'from', 'further', 'gave', 'gets', 'give',
 'given', 'giving', 'gone', 'got', 'had', 'hardly', 'has', 'have', 'having',
 'here', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'itself',
 'just', 'keep', 'kept', 'knowledge', 'largely', 'like', 'made', 'mainly',
 'make', 'many', 'might', 'more', 'most', 'mostly', 'much', 'must', 'nearly',
 'necessarily', 'neither', 'next', 'no', 'none', 'nor', 'normally', 'not',
 'noted', 'now', 'obtain', 'obtained', 'of', 'often', 'on', 'only', 'or',
 'other', 'our', 'out', 'owing', 'particularly', 'past', 'perhaps', 'please',
 'poorly', 'possible', 'possibly', 'potentially', 'predominantly', 'present',
 'previously', 'primarily', 'probably', 'prompt', 'promptly', 'put',
 'quickly', 'quite', 'rather', 'readily', 'really', 'recently', 'regarding',
 'regardless', 'relatively', 'respectively', 'resulted', 'resulting',
 'results', 'said', 'same', 'seem', 'seen', 'several', 'shall', 'should',
 'show', 'showed', 'shown', 'shows', 'significantly', 'similar', 'similarly',
 'since', 'slightly', 'so', 'some', 'sometime', 'somewhat', 'soon',
 'specifically', 'state', 'states', 'strongly', 'substantially',
 'successfully', 'such', 'sufficiently', 'than', 'that', 'the', 'their',
 'theirs', 'them', 'then', 'there', 'therefore', 'these', 'they', 'this',
 'those', 'though', 'through', 'throughout', 'to', 'too', 'toward', 'under',
 'unless', 'until', 'up', 'upon', 'use', 'used', 'usefully', 'usefulness',
 'using', 'usually', 'various', 'very', 'was', 'we', 'were', 'what', 'when',
 'where', 'whether', 'which', 'while', 'who', 'whose', 'why', 'widely',
 'will', 'with', 'within', 'without', 'would', 'yet', 'you'])

def to_query_string(str):
  words = str.lower().strip().split()
  keywords = filter(lambda x: x not in IGNORE_WORDS, words)
  return " OR ".join( map(lambda x: "~" + x, keywords) )
