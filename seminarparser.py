import re

def extract_entities_iter(tagged_text):
    """
	convert tagged text in the nist.gov format into a generator yielding
	(entitytype, entitystring) tuples.

	e.g. Hello <ENAMEX TYPE="PERSON">Jim</ENAMEX>, how are you?

	Would yield:

	('PERSON', 'Jum')

    :param tagged_text: tagged text in the nist.gov format
    :return generator of (entitytype, entitystring) tuples
	"""

    open_close_match = '<[^>\/]+>[^<>]+<\/[^>]+>'
    # matches an opening tag, contents and closing tag

    open_close_matches = re.findall(open_close_match, tagged_text)
    # our opening tag, contents and closing tag

    for match in open_close_matches:
        yield match