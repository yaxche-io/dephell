# built-in
from collections import OrderedDict

# external
import tomlkit

# app
from ..models import Constraint, Dependency, RootDependency
from ..repositories import WareHouseRepo, get_repo
from .base import BaseConverter


VCS_LIST = ('git', 'svn', 'hg', 'bzr')


class PIPFileConverter(BaseConverter):
    lock = False
    fields = (
        'version', 'editable', 'extras', 'markers',
        'ref', 'vcs', 'index', 'hashes',
        'subdirectory', 'path', 'file', 'uri',
        'git', 'svn', 'hg', 'bzr',
    )

    def loads(self, content) -> RootDependency:
        doc = tomlkit.parse(content)
        deps = []
        root = RootDependency(self._get_name(content=content))

        repos = dict()
        if 'source' in doc:
            for repo in doc['source']:
                repos[repo['name']] = repo['url']

        if 'packages' in doc:
            for name, content in doc['packages'].items():
                dep = self._make_dep(root, name, content)
                if 'index' in content:
                    repo_name = content.get('index')
                    dep.repo = WareHouseRepo(
                        name=repo_name,
                        url=repos[repo_name],
                    )
                deps.append(dep)
        root.attach_dependencies(deps)
        return root

    def dumps(self, reqs, project: RootDependency, content=None) -> str:
        if content:
            doc = tomlkit.parse(content)
        else:
            doc = tomlkit.document()

        if 'source' not in doc:
            doc['source'] = tomlkit.aot()

        added_repos = {repo['name'] for repo in doc['source']}
        for req in reqs:
            if not isinstance(req.dep.repo, WareHouseRepo):
                continue
            if req.dep.repo.name in added_repos:
                continue
            added_repos.add(req.dep.repo.name)
            doc['source'].append(OrderedDict([
                ('name', req.dep.repo.name),
                ('url', req.dep.repo.url),
                ('verify_ssl', True),
            ]))

        if 'packages' in doc:
            # clean packages from old packages
            names = {req.name for req in reqs}
            doc['packages'] = {
                name: info
                for name, info in doc['packages'].items()
                if name in names
            }
            # write new packages to this table
            packages = doc['packages']
        else:
            packages = tomlkit.table()

        for req in reqs:
            packages[req.name] = self._format_req(req=req)
        doc['packages'] = packages

        return tomlkit.dumps(doc)

    # https://github.com/pypa/pipfile/blob/master/examples/Pipfile
    @staticmethod
    def _make_dep(root, name: str, content) -> Dependency:
        if isinstance(content, str):
            return Dependency(
                raw_name=name,
                constraint=Constraint(root, content),
                repo=get_repo(),
            )

        # get link
        url = content.get('file') or content.get('path') or content.get('vcs')
        if not url:
            for vcs in VCS_LIST:
                if vcs in content:
                    url = vcs + '+' + content[vcs]
                    break
        if 'ref' in content:
            url += '@' + content['ref']

        # https://github.com/sarugaku/requirementslib/blob/master/src/requirementslib/models/requirements.py
        # https://github.com/pypa/pipenv/blob/master/pipenv/project.py
        return Dependency.from_params(
            raw_name=name,
            # https://github.com/sarugaku/requirementslib/blob/master/src/requirementslib/models/utils.py
            constraint=Constraint(root, content.get('version', '')),
            extras=set(content.get('extras', [])),
            marker=content.get('markers'),
            url=url,
            editable=content.get('editable', False),
        )

    def _format_req(self, req):
        result = tomlkit.inline_table()
        for name, value in req:
            if name == 'rev':
                name = 'ref'
            if name in self.fields:
                if isinstance(value, tuple):
                    value = list(value)
                result[name] = value
        if 'version' not in result:
            result['version'] = '*'
        # if we have only version, return string instead of table
        if tuple(result.value) == ('version', ):
            return result['version']
        # do not specify version explicit
        if result['version'] == '*':
            del result['version']

        return result